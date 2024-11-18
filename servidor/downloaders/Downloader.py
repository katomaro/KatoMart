import time
import pathlib
import requests
import yt_dlp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from servidor.models.configs import Configuration
import copy
import re
import m3u8
import os
import shutil
import subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import requests


def ytdlp_download_pandavideos(course_url, url, output_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
               'Referer': course_url,
               'Origin': course_url + '/'}
    ydl_opts = {
        'format': 'bv+ba/b',
        'outtmpl': output_name,
        'http_headers': headers,
        'referer': course_url,
        'concurrent_fragment_downloads': 10,
        'fragment_retries': 50,
        'retry_sleep_functions': {'fragment': 30},
        'retries': 30,
        'extractor_retries': 10,        
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def fix_pandavideos_url(video_url):
    if video_url.endswith('/playlist.m3u8'):
        return video_url
    pattern = r'v=([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[1-5][a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})'
    match = re.search(pattern, video_url)
    if match:
        extracted_part = match.group(1)
        if 'embed' in video_url:
            video_url = f'{video_url.rsplit('/embed/', 1)[0]}/{extracted_part}/playlist.m3u8'

    return video_url


class Downloader:
    def __init__(self, db_session, session=None, driver=None):
        """
        Initialize the Downloader class.

        Parameters:
        - db_session: SQLAlchemy session object to interact with the database.
        - session (optional): An instance of requests.Session to use for HTTP requests.
        - driver (optional): An instance of Selenium WebDriver to use for automated browser interactions.
        """
        self.db_session = db_session
        self.config = self.load_configurations()
        self.session = self.clone_requests_session(session) if session else requests.Session()
        self.setup_session_headers()
        self.driver = driver
        self.ytdlp_options = self.get_ytdlp_options()
        self.allowed_file_types = self.get_allowed_file_types()
        self.max_retries = int(self.config.get('download_maximum_retries_per_file', 5))
        self.download_await_time = int(self.config.get('download_await_time', 5))
        self.download_await_on_fail = int(self.config.get('download_await_on_fail', 60))

    def clone_requests_session(self, session):
        """Create a deep copy of a requests.Session object."""
        new_session = requests.Session()
        new_session.headers = session.headers.copy()
        new_session.cookies = requests.cookies.cookiejar_from_dict(
            requests.utils.dict_from_cookiejar(session.cookies)
        )
        new_session.auth = copy.deepcopy(session.auth)
        new_session.proxies = copy.deepcopy(session.proxies)
        new_session.hooks = copy.deepcopy(session.hooks)
        new_session.params = copy.deepcopy(session.params)
        new_session.verify = copy.deepcopy(session.verify)
        new_session.cert = copy.deepcopy(session.cert)
        # Adapters need special handling; re-instantiate them
        for prefix, adapter in session.adapters.items():
            new_session.mount(prefix, copy.deepcopy(adapter))
        return new_session

    def load_configurations(self):
        """Load configurations from the database and cast them to appropriate types."""
        configs = self.db_session.query(Configuration).all()
        config_dict = {}
        for config in configs:
            key = config.key
            value = config.value
            if config.value_type == 'int':
                value = int(value)
            elif config.value_type == 'bool':
                value = True if str(value).lower() in ['true', '1'] else False
            elif config.value_type == 'float':
                value = float(value)
            config_dict[key] = value
        return config_dict

    def setup_session_headers(self):
        """Set up the headers for the requests session."""
        user_agent = self.config.get('default_user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0')
        self.session.headers.update({'User-Agent': user_agent})

    def get_ytdlp_options(self):
        """Prepare yt-dlp options from configurations."""
        ytdlp_options = {}
        for key, value in self.config.items():
            if key.startswith('ytdlp_'):
                ytdlp_option = key.replace('ytdlp_', '')
                ytdlp_options[ytdlp_option] = value
        return ytdlp_options

    def get_allowed_file_types(self):
        """Return a set of allowed file extensions based on configurations."""
        allowed_file_types = set()
        for key, value in self.config.items():
            if key.startswith('file_type_') and value:
                file_extension = key.replace('file_type_', '')
                allowed_file_types.add(file_extension.lower())
        return allowed_file_types

    def download_file(self, url, destination_path, referer=None):
        """Download a single file using the appropriate method."""
        # Get the file extension
        file_extension = pathlib.Path(destination_path).suffix.replace('.', '').lower()
        if file_extension and file_extension not in self.allowed_file_types:
            print(f"Skipping download of {url}, file type '{file_extension}' not allowed.")
            return

        # Decide which method to use for downloading
        prefer_ytdlp = self.config.get('stream_prefer_ytdlp', False)
        if prefer_ytdlp and self.is_ytdlp_supported(url):
            self.download_with_ytdlp(url, destination_path, referer=referer)
        elif self.driver:
            self.download_with_selenium(url, destination_path)
        else:
            self.download_with_requests(url, destination_path)

    def is_ytdlp_supported(self, url):
        """Check if yt-dlp supports the given URL."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                ydl.extract_info(url, download=False)
                return True
        except yt_dlp.utils.DownloadError:
            return False

    def download_with_ytdlp(self, url, destination_path, referer=None):
        """Download the file using yt-dlp."""
        ydl_opts = self.ytdlp_options.copy()
        ydl_opts['outtmpl'] = destination_path
        ydl_opts['retries'] = self.config.get('ytdlp_retries', 5)
        ydl_opts['concurrent_fragment_downloads'] = self.config.get('ytdlp_concurrent_fragments', 3)

        # Pass session cookies and headers to yt-dlp if needed
        # For example, use 'cookiefile' or 'cookiesfrombrowser' options if applicable

        # Pass session headers to yt-dlp
        # cookies = self.session.cookies.get_dict()
        # cookie_string = '; '.join([f'{key}={value}' for key, value in cookies.items()])
        # ydl_opts['http_headers'] = self.session.headers.copy()
        # ydl_opts['http_headers']['Cookie'] = cookie_string

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                if referer:
                    ydl.params['http_headers'] = {'Referer': referer}
                ydl.download([url])
            except Exception as e:
                print(f"Error downloading {url} with yt-dlp: {e}")
                raise

    def download_with_selenium(self, url, destination_path):
        """Download the file using Selenium WebDriver."""
        raise NotImplementedError("Selenium download is not implemented yet.")

    def download_with_requests(self, url, destination_path):
        """Download the file using the requests library, handling retries."""
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.session.get(url, stream=True, timeout=30)
                response.raise_for_status()
                with open(destination_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                break
            except Exception as e:
                retries += 1
                print(f"Error downloading {url} with requests (attempt {retries}/{self.max_retries}): {e}")
                if retries >= self.max_retries:
                    print(f"Failed to download {url} after {self.max_retries} retries.")
                    raise
                else:
                    time.sleep(self.download_await_on_fail)

    def ts_to_mp4(self, input_file, output_file):
        """
        Convert TS file to MP4 using ffmpeg.

        :param input_file: The input TS file path.
        :param output_file: The output MP4 file path.
        """
        output_file = pathlib.Path(output_file)
        if output_file.suffix.lower() != '.mp4':
            output_file = output_file.with_suffix('.mp4')
        
        input_file = os.path.abspath(input_file)
        output_file = os.path.abspath(output_file)

        # print(f"Converting {input_file} to {output_file}")
        ffmpeg_path = self.config.get('ffmpeg_path', 'ffmpeg')  # Default to 'ffmpeg' in PATH
        try:
            subprocess.run([ffmpeg_path, '-hide_banner', '-loglevel', 'error', '-y', '-i', input_file, '-c', 'copy', output_file], check=True)
            os.remove(input_file)
        except Exception as e:
            print(f"Error converting {input_file} to {output_file}: {e}")


    def decrypt_segment(self, content, key, iv):
        """
        Decrypt a media segment using AES-128 CBC.

        :param content: Encrypted content of the segment.
        :param key: The decryption key.
        :param iv: The initialization vector.
        :return: Decrypted content of the segment.
        """
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(content) + decryptor.finalize()
        return decrypted_data


    def download_with_retries(self, file_url, headers=None):
        """
        Try to download a file with retries.

        :param file_url: URL of the file to download.
        :param headers: Optional headers to include in the request.
        :return: The content of the file in bytes, or None if failed.
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(file_url, headers=headers, timeout=60)
                return response.content
            except requests.RequestException as e:
                print(f"Error downloading {file_url}, attempt {attempt + 1} of {self.max_retries}: {e}")
                time.sleep(self.download_await_on_fail)
        print(f"Failed to download {file_url} after {self.max_retries} attempts.")
        return None
    
    def download_hls_variant_playlist(self, url, destination_path, referer=None, headers=None):
        """
        Download HLS variant playlist and save to destination_path.

        :param url: URL of the variant playlist (.m3u8 file).
        :param destination_path: The output file path where the final video will be saved.
        :param referer: Optional referer header value.
        """
        hheaders = self.session.headers.copy()
        if referer:
            hheaders['Referer'] = referer
            hheaders['Origin'] = referer.rsplit('/', 1)[0]

        if headers:
            hheaders.update(headers)

        # Download the variant playlist
        variant_playlist_content = self.download_with_retries(url, headers=headers)
        if variant_playlist_content is None:
            print(f"Failed to download variant playlist from {url}")
            return

        # Parse the variant playlist
        # print('1' * 50)
        # print('1' * 50)
        # print('1' * 50)
        # print(variant_playlist_content.decode('utf-8'))
        # print('1' * 50)
        # print('1' * 50)
        # print('1' * 50)
        variant_playlist = m3u8.loads(variant_playlist_content.decode('utf-8'))
        # Handle decryption keys
        key = None
        iv = None
        if variant_playlist.keys and variant_playlist.keys[0]:
            key_info = variant_playlist.keys[0]
            # print('2' * 50)
            # print('key uri')
            # print(key_info.uri)
            # print('2' * 50)
            key_uri = key_info.uri
            key_content = self.download_with_retries(key_uri, headers=headers)
            if key_content is None:
                print(f"Failed to download decryption key from {key_uri}")
                return
            key = key_content
            if key_info.iv:
                iv = bytes.fromhex(key_info.iv.replace('0x', '').zfill(32))
            else:
                iv = None  # Will be handled per segment

        # Prepare a temporary directory to store segments
        temp_dir = 'temp_segments'
        os.makedirs(temp_dir, exist_ok=True)

        segment_files = []
        base_url = url.rsplit('/hls/', 1)[0] + '/hls/'
        for idx, segment in enumerate(variant_playlist.segments):
            segment_url = base_url + segment.uri
            segment_content = self.download_with_retries(segment_url, headers=headers)
            if segment_content is None:
                print(f"Failed to download segment from {segment_url}")
                return

            if key:
                if not iv:
                    sequence_number = segment.media_sequence or idx
                    iv_int = sequence_number.to_bytes(16, byteorder='big')
                    segment_iv = iv_int
                else:
                    segment_iv = iv
                decrypted_segment = self.decrypt_segment(segment_content, key, segment_iv)
            else:
                decrypted_segment = segment_content

            segment_filename = os.path.join(temp_dir, f"segment_{idx}.ts")
            with open(segment_filename, 'wb') as f:
                f.write(decrypted_segment)

            segment_files.append(segment_filename)

            # Progress feedback
            if (idx + 1) % 10 == 0 or (idx + 1) == len(variant_playlist.segments):
                print(f"Downloaded {idx + 1}/{len(variant_playlist.segments)} segments.")

        # Concatenate segments using ffmpeg
        concatenated_filename = os.path.join(temp_dir, 'concatenated.ts')
        self.concatenate_segments_ffmpeg(segment_files, concatenated_filename)

        # Convert to MP4 if necessary
        self.ts_to_mp4(concatenated_filename, destination_path)

        # Clean up temporary files
        shutil.rmtree(temp_dir)

    def concatenate_segments_ffmpeg(self, segment_files, output_file):
        """
        Concatenate TS segments using ffmpeg.

        :param segment_files: List of segment file paths.
        :param output_file: Output file path for the concatenated TS file.
        """
        ffmpeg_path = self.config.get('ffmpeg_path', 'ffmpeg')  # Use 'ffmpeg' from PATH by default

        # Create a file listing all segment files
        concat_file = 'concat_list.txt'
        with open(concat_file, 'w') as f:
            for segment_file in segment_files:
                f.write(f"file '{os.path.abspath(segment_file)}'\n")

        # Run ffmpeg to concatenate
        command = [ffmpeg_path, '-hide_banner', '-loglevel', 'error', '-fflags', '+genpts', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', '-copyts', '-start_at_zero', output_file]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error concatenating segments: {e}")
            raise
        finally:
            os.remove(concat_file)


    def download_hls_playlist(self, url, destination_path, referer=None):
        """Download HLS playlist and save to destination_path."""
        headers = self.session.headers.copy()
        if referer:
            headers['Referer'] = referer

        # Download the master playlist
        master_playlist_content = self.download_with_retries(url, headers=headers)
        if master_playlist_content is None:
            print(f"Failed to download master playlist from {url}")
            return

        # Parse the master playlist
        master_playlist = m3u8.loads(master_playlist_content.decode('utf-8'), uri=url)

        # Sort the variants by bandwidth
        sorted_variants = sorted(master_playlist.playlists, key=lambda x: x.stream_info.bandwidth, reverse=True)
        best_variant = sorted_variants[0]
        variant_url = best_variant.absolute_uri
        print(f"Selected variant with bandwidth {best_variant.stream_info.bandwidth}: {variant_url}")

        # Download the variant playlist
        variant_playlist_content = self.download_with_retries(variant_url, headers=headers)
        if variant_playlist_content is None:
            print(f"Failed to download variant playlist from {variant_url}")
            return

        # Parse the variant playlist
        variant_playlist = m3u8.loads(variant_playlist_content.decode('utf-8'), uri=variant_url)

        # Handle decryption
        key = None
        iv = None
        if variant_playlist.keys and variant_playlist.keys[0]:
            key_info = variant_playlist.keys[0]
            key_uri = key_info.absolute_uri
            key_content = self.download_with_retries(key_uri, headers=headers)
            if key_content is None:
                print(f"Failed to download decryption key from {key_uri}")
                return
            key = key_content
            if key_info.iv:
                iv = bytes.fromhex(key_info.iv.replace('0x', '').zfill(32))
            else:
                iv = None  # Will be handled per segment

        # Download and decrypt segments
        segment_files = []
        for idx, segment in enumerate(variant_playlist.segments):
            segment_url = segment.absolute_uri
            segment_content = self.download_with_retries(segment_url, headers=headers)
            if segment_content is None:
                print(f"Failed to download segment from {segment_url}")
                return

            if key:
                # Use per-segment IV if not specified
                if not iv:
                    # IV is the segment's media sequence number represented as a 16-byte big-endian integer
                    sequence_number = segment.media_sequence or idx
                    iv_int = sequence_number.to_bytes(16, byteorder='big')
                    segment_iv = iv_int
                else:
                    segment_iv = iv
                decrypted_segment = self.decrypt_segment(segment_content, key, segment_iv)
            else:
                decrypted_segment = segment_content

            segment_filename = f"segment_{idx}.ts"
            with open(segment_filename, 'wb') as f:
                f.write(decrypted_segment)

            segment_files.append(segment_filename)

        # Concatenate segments
        concatenated_filename = (destination_path.rsplit('/', 1)[0]+'/') + 'concatenated.ts'
        with open(concatenated_filename, 'wb') as outfile:
            for fname in segment_files:
                with open(fname, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

        # Convert to MP4 if necessary
        self.ts_to_mp4(concatenated_filename, destination_path)

        # Clean up segment files
        for fname in segment_files:
            os.remove(fname)
        os.remove(concatenated_filename)