import json
import os
import pathlib
import re
import shutil
import time

from bs4 import BeautifulSoup
import m3u8
import requests
import yt_dlp

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

from modules.accounts.abstract import Account



def remover_caracteres_problematicos(name:str) -> str:
    """
    Remove os caracteres conhecidos como problemáticos em nomes de arquivos.
    """
    # Windows: <>:"/\|?*
    sanitized = re.sub(r'[<>:"/\\|?*]+', '', name)
    sanitized = sanitized.strip()
    return sanitized

# TODO: Refatorar todos os requests para usar a sessão da conta
# TODO: Alterar os prints para um database.log ou um logger
# TODO: Alterar todas as strings para Pathlib.Path para garantir uma manipulação de arquivos segura e universal

class Downloader:
    def __init__(self, account: Account=None) -> None:
        self.account = account

        self.request_session: requests.Session = None

        # Current Content Information
        self.current_content_id = None
        self.current_content_name = None
        self.current_content_url = None
        self.current_content_progress = None
        self.current_module_id = None
        self.current_module_name = None
        self.current_module_progress = None
        self.current_lesson_id = None
        self.current_lesson_name = None
        self.current_lesson_progress = None

        self.total_courses = 0
        self.completed_courses = 0
        self.total_modules = 0
        self.completed_modules = 0
        # Este atributo não é bom a nível global, impreciso.
        self.total_lessons = 0
        self.completed_lessons = 0
        # Este atributo não é bom a nível global, impreciso.
        self.total_files = 0
        self.completed_files = 0

        self.url_download = None
        self.download_path = pathlib.Path('.')
        self.current_base_playlist_url = None
        self.selected_quality_url = None
        self.total_segments = 0
        self.downloaded_segments = 0
        self.key_content = None
        self.key_iv = None
        self.file_name = None
        self.media_id = None
        self.media_size = None
        self.media_duration_secs = None
        self.media_url = None

        # General Download Settings
        self.download_subtitles = False
        self.subtitle_language = None
        self.download_quality = None
        self.download_quality_fallback = None
        self.download_interval = 0
        self.download_retries = 3
        self.download_segments_in_order = True
        self.download_timeout = 30
        self.use_original_media_name = False
        self.download_widevine = False
        self.widevine_cdm_path = pathlib.Path('.')
        self.bento4_toolbox_path = pathlib.Path('.')
        self.scan_html_for_videos = False
        self.use_custom_ffmpeg = False
        self.custom_ffmpeg_path = pathlib.Path('.')
        self.download_threads = 1

        # Player Download selection
        self.download_from_sources = {}

        # DRM Types to Download
        self.download_drm_types = {}

        # Media Types to Download
        self.download_content_types = {}

        self.widevine_key_mappings = {}

        self.load_settings()

        self.iter_account_contents()


    def load_settings(self):
        """
        Carrega as configurações do banco de dados.
        """
        # General Settings
        settings = self.account.database_manager.get_all_settings()
        self.download_subtitles = settings['download_subtitles']
        self.subtitle_language = settings['subtitle_language']
        self.download_quality = settings['download_quality']
        self.download_quality_fallback = settings['download_quality_fallback']
        self.download_interval = float(settings['download_interval'])
        self.download_retries = int(settings['download_retries'])
        self.download_segments_in_order = bool(settings['download_segments_in_order'])
        self.download_timeout = float(settings['download_timeout'])
        self.use_original_media_name = settings['use_original_media_name']
        self.download_widevine = settings['download_widevine']
        self.widevine_cdm_path = pathlib.Path(settings['widevine_cdm_path'])
        self.bento4_toolbox_path = pathlib.Path(settings['bento4_toolbox_path'])
        self.scan_html_for_videos = bool(settings['scan_html_for_videos'])
        self.use_custom_ffmpeg = bool(settings['use_custom_ffmpeg'])
        self.custom_ffmpeg_path = pathlib.Path(settings['custom_ffmpeg_path'])
        self.download_threads = settings['download_threads']

        # Delivery Sources
        delivery_sources = self.account.database_manager.get_all_media_delivery_sources()
        self.download_from_sources = delivery_sources

        # DRM Types
        drm_types = self.account.database_manager.get_all_drm_types()
        self.download_drm_types = drm_types

        # Media Content Types to download
        content_types = self.account.database_manager.get_all_media_types()
        self.download_content_types = content_types

    def iter_account_contents(self):
        """
        Itera sobre os conteúdos de uma conta.
        """
        # Aqui a gente assume que o método da conta organizou todo o conteúdo, então não precisamos ir buscar informaçções
        # Pode vir ser necessário no futuro, então... TODO: Implementar um chamada para buscar informações precisas
        for content in self.account.downloadable_products:
            download_path = pathlib.Path(content.get('save_path'))
            content = content.get('data')
            self.current_content_id = content['id']
            self.current_content_url = content['domain']
            download_path = download_path / remover_caracteres_problematicos(content['name'])
            if not download_path.exists():
                download_path.mkdir(parents=True)
            self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Baixando conteúdo: {content['name']} ^-^ {self.account.account_id} - {self.account.get_platform_id()}")
            if not content.get('modules'):
                self.get_content_modules()
            for module in content.get('modules'):
                self.current_module_id = module['id']
                module_path = download_path / remover_caracteres_problematicos(f"{module['moduleOrder']}. " + module['name'])
                if not module.get('lessons'):
                    self.get_content_lessons()
                for lesson in module.get('lessons'):
                    self.current_lesson_id = lesson['id']
                    lesson_path = module_path / remover_caracteres_problematicos(f"{lesson['lessonOrder']}. " + lesson['name'])
                    if not lesson.get('files'):
                        lesson['files'] = self.get_content_files()
                    if lesson.get('files'):
                        if not lesson_path.exists():
                            lesson_path.mkdir(parents=True)
                        lesson_files = lesson.get('files')

                        if lesson_files.get('text_content'):
                            file_name = 'Conteúdo_Textual.html'
                            with open(lesson_path / file_name, 'w', encoding='utf-8') as f:
                                f.write(lesson_files['text_content'])

                        if lesson_files.get('references'):
                            file_name = 'Referências.txt'
                            with open(lesson_path / file_name, 'w', encoding='utf-8') as f:
                                for reference in lesson_files['references']:
                                    f.write(f"{reference}\n")

                        if lesson_files.get('medias'):
                            for media_index, media in enumerate(lesson_files['medias'], start=1):
                                media_name = f"{media_index}. {media['name']}"
                                self.download_content(media, lesson_path, media_name, is_attachment=False)

                        if lesson_files.get('attachments'):
                            for attachment_index, attachment in enumerate(lesson_files['attachments']):
                                attachment_name = f"{attachment_index}. {attachment['name']}"
                                self.download_content(attachment, lesson_path, attachment_name, is_attachment=True)

    def get_content_modules(self):
        """
        Busca os módulos de um conteúdo.
        """
        pass

    def get_content_lessons(self):
        """
        Busca as lições de um módulo.
        """
        pass

    def get_content_files(self):
        """
        Busca os arquivos de uma lição.
        """
        data = self.account.get_content_lesson_info(self.current_content_id,
                                                    self.current_content_url,
                                                    self.current_module_id,
                                                    self.current_lesson_id)
        return data

    def download_content(self, file: any, download_path:str, file_name:str, is_attachment:bool=False):
        """
        Baixa um conteúdo de uma URL.
        """
        self.download_path = download_path
        if not is_attachment:
            self.file_name = file_name.rsplit('.', 1)[0] + '.ts'
        else:
            self.file_name = file_name
            input(file)
        self.media_id = file.get('hash')
        self.media_size = file.get('size')
        self.media_duration_secs = file.get('duration')
        self.media_url = file.get('url')
        if file.get('is_stream'):
            self.get_video_playlist()
        else:
            self.download_raw_file()

    def get_video_playlist(self):
        """
        Baixa a playlist de vídeo m3u8.
        """
        is_stream = False
        has_drm = False
        data = {}
        self.request_session = self.account.clone_main_session()
        self.request_session.headers['Referer'] = self.current_content_url

        response = self.request_session.get(self.media_url)
        if response.status_code != 200:
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=1, log_data=f"Erro ao baixar a playlist de vídeo: {self.media_url}")
            return

        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            data = response.json()

        if 'text/html' in content_type:
            html_content = response.text
            data = self.handle_html_response(html_content)

        if data['transmission_type'].lower() in ('vod'):
            is_stream = True

        if data['media_has_drm']:
            has_drm = True
            # self.download_widevine_media()

        current_master_playstlist_content = None
        playlist_url = ''
        if len(data['media_assets']) > 0:
            for asset in data['media_assets']:
                playlist_url = asset.get('url')
                self.current_base_playlist_url = playlist_url.rsplit('/', 1)[0] +'/'
                current_master_playstlist_content = self.load_playlist(playlist_url)

            playlist = m3u8.loads(current_master_playstlist_content)
            if self.download_subtitles:
                if self.subtitle_language.lower() == 'all':
                    subtitles = [media for media in playlist.media if media.type == 'SUBTITLES']
                    for subtitle in subtitles:
                        with open(self.download_path / (self.file_name + f"_{subtitle.language}.vtt"), 'wb') as f:
                            actual_sub = self.request_session.get(self.current_base_playlist_url + subtitle.uri)
                            subtitle_content = m3u8.loads(actual_sub.text)
                            sub_ct = self.request_session.get(self.current_base_playlist_url + subtitle_content.segments[0].uri)
                            f.write(sub_ct.content)

            if playlist.is_variant:
                highest_bandwidth = 0
                best_quality_playlist = None
                for variant in playlist.playlists:
                    if variant.stream_info.bandwidth > highest_bandwidth:
                        highest_bandwidth = variant.stream_info.bandwidth
                        best_quality_playlist = variant
                self.current_base_playlist_url = playlist_url.rsplit('/', 1)[0] +'/'
                playlist = m3u8.loads(self.load_playlist(self.current_base_playlist_url + best_quality_playlist.uri))
                self.selected_quality_url = best_quality_playlist.uri

            if playlist.keys:
                self.download_encrypted_hls(playlist)
            else:
                self.download_raw_hls(playlist)

    def load_playlist(self, playlist_url:str) -> str:
        """
        Carrega a playlist mestre de um vídeo.
        """
        response = self.request_session.get(playlist_url)
        if response.status_code != 200:
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=1, log_data=f"Erro ao baixar a playlist mestre: {playlist_url}")

        return response.text

    def handle_html_response(self, html_content:str) -> dict:
        """
        Lida com uma resposta HTML usando o BeautifulSoup.
        """
        filtered_html = {}
        soup = BeautifulSoup(html_content, 'html.parser')
        if self.account.get_platform_id() == 1:
            # Hotmart Specific HTML Parsing
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if script_tag:
                data = json.loads(script_tag.string)
                application_data = data.get('props', {}).get('pageProps', {}).get('applicationData', {})
                media_has_drm = application_data.get('isDrmEnabled', False)
                is_media_public = application_data.get('isMediaPublic', False)
                needs_jwt = application_data.get('isJwtSignature', False)
                media_type = application_data.get('mediaType', '')
                transmission_type = application_data.get('transmissionType', '')
                media_flags = {}
                flags = application_data.get('flags', {})
                media_flags['ENABLE_PLAYER_V4_ENCRYPTION'] = flags.get('ENABLE_PLAYER_V4_ENCRYPTION', False)
                media_flags['ENABLE_PLAYER_DISPLAY_USER_ID'] = flags.get('ENABLE_PLAYER_DISPLAY_USER_ID', False)  # Fake DRM lmao
                media_flags['ENABLE_PLAYER_V4_API'] = flags.get('ENABLE_PLAYER_V4_API', False)
                media_flags['ENABLE_PLAYER_FINGER_PRINT'] = flags.get('ENABLE_PLAYER_FINGER_PRINT', False)  # Could be dangerous
                media_code = application_data.get('mediaCode', '')
                application_key = application_data.get('applicationKey', '')
                media_membership_id = application_data.get('clubMembershipId', '')
                mux_api_key = application_data.get('muxApiKey', '')
                thumbnail_url = application_data.get('thumbnailUrl', '')
                media_assets = application_data.get('mediaAssets', [])
                finish_transcode_date = application_data.get('finishTranscodeDate', '')
                cdn_provider = application_data.get('cdnProvider', '')
                user_code = application_data.get('userCode', '')
                signature = application_data.get('signature', '')
                api_version = application_data.get('apiVersion', '')  # Currently v5
                platform_user_id = application_data.get('platformUserId', '')
                media_query = application_data.get('query', '')
                media_build_id = application_data.get('buildId', '')
                asset_prefix = application_data.get('assetPrefix', '')
                is_fallback = application_data.get('isFallback', False)

                # Retorno dos dados filtrados, necessário globalizar depois
                filtered_html['media_has_drm'] = media_has_drm
                filtered_html['is_media_public'] = is_media_public
                filtered_html['needs_jwt'] = needs_jwt
                filtered_html['media_type'] = media_type
                filtered_html['transmission_type'] = transmission_type
                filtered_html['media_flags'] = media_flags
                filtered_html['media_code'] = media_code
                filtered_html['application_key'] = application_key
                filtered_html['media_membership_id'] = media_membership_id
                filtered_html['mux_api_key'] = mux_api_key
                filtered_html['thumbnail_url'] = thumbnail_url
                filtered_html['media_assets'] = media_assets
                filtered_html['finish_transcode_date'] = finish_transcode_date
                filtered_html['cdn_provider'] = cdn_provider
                filtered_html['user_code'] = user_code
                filtered_html['signature'] = signature
                filtered_html['api_version'] = api_version
                filtered_html['platform_user_id'] = platform_user_id
                filtered_html['media_query'] = media_query
                filtered_html['media_build_id'] = media_build_id
                filtered_html['asset_prefix'] = asset_prefix
                filtered_html['is_fallback'] = is_fallback

        return filtered_html

    def download_raw_hls(self, playlist: m3u8.M3U8):
        """
        Baixa o arquivo m3u8 e os segmentos de vídeo.
        """
        for segment in playlist.segments:
            segment_url = segment.uri
            if not segment_url.startswith('http'):
                segment_url = self.current_base_playlist_url + self.selected_quality_url.split('/', 1)[0] + '/' + segment.uri

            content = self.download_segment()
            if content:
                with open(self.download_path / self.file_name, 'a+b') as f:
                    f.write(content)

    def download_encrypted_hls(self, playlist: m3u8.M3U8):
        """
        Baixa o arquivo m3u8 e os segmentos de vídeo criptografados.
        """
        if playlist.keys:
            for key in playlist.keys:
                if key:  # Se existir uma chave na playlist
                    key_uri = key.uri
                    self.key_content = self.request_session.get(self.current_base_playlist_url + self.selected_quality_url.split('/', 1)[0] + '/' + key_uri).content  # Baixa a chave de encriptação
                    self.key_iv = key.iv  # Pode ser None, neste caso você pode querer gerar um IV baseado no número do segmento ou usar um IV padrão
                    if self.key_iv:
                        self.key_iv = bytes.fromhex(self.key_iv[2:])  # Remove o prefixo '0x' e converte para bytes
                    else:
                        # Aqui você precisaria definir um IV padrão ou gerar um baseado no segmento
                        self.key_iv = b'\x00' * 16  # Exemplo de IV padrão
                    break  # Este exemplo assume apenas uma chave para todos os segmentos

            for segment in playlist.segments:
                segment_url = segment.uri
                if not segment_url.startswith('http'):
                    segment_url = self.current_base_playlist_url + self.selected_quality_url.split('/', 1)[0] + '/' + segment.uri

                content = self.download_segment(segment_url)
                if content and self.key_content:
                    content = self.decrypt_segment(content)
                    with open(self.download_path / self.file_name, 'a+b') as f:
                        f.write(content)

    def download_raw_file(self):
        """
        Baixa um arquivo diretamente.
        """
        # TODO: Implementar o download de arquivos diretamente
        response = self.request_session.get(self.media_url)
        if response.status_code == 200:
            with open(self.download_path / self.file_name, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Erro ao baixar o arquivo: {self.url_download}")

    def download_ytdlp_media(self, url:str, referer:str=None, save_path:str=None):
        """
        Baixa um vídeo ou playlist de vídeos do YouTube usando yt-dlp.
        """
        ytdlp_opts = {'retries': 8,
                'fragment_retries': 6,
                'quiet': True,
                "outtmpl": save_path}
        with yt_dlp.YoutubeDL(ytdlp_opts) as ytdlp:
            if referer:
                ytdlp.params['http_headers'] = {'Referer': referer}
            ytdlp.download([url])

    def download_widevine_media(self, url:str, save_path:str):
        """
        Baixa um vídeo protegido por Widevine.
        """
        print('Desejo a todas inimigas vida longa')

    def download_segment(self, segment_url:str = ''):
        """
        Tenta baixar um segmento com um determinado número de retentativas.
        
        :param segment_url: URL do segmento a ser baixado.
        :param max_retries: Número máximo de retentativas.
        :param delay_between_retries: Tempo de espera entre retentativas, em segundos.
        :return: O conteúdo do segmento, se o download for bem-sucedido; None, caso contrário.
        """
        for attempt in range(self.download_retries):
            try:
                response = self.request_session.get(segment_url, timeout=self.download_timeout)
                response.raise_for_status()
                return response.content
            except requests.RequestException as e:
                print(f"Erro ao baixar {segment_url}, tentativa {attempt + 1} de {self.download_retries}. Erro: {e}")
                time.sleep(self.download_timeout)
        print(f"[DOWNLOADER] Falha ao baixar o segmento após {self.download_retries} tentativas: {segment_url}")
        return None

    def decrypt_segment(self, content:bytes) -> bytes:
        """
        Descriptografa um segmento de mídia usando AES.
        
        :param content: O conteúdo criptografado do segmento.
        :param key: A chave de criptografia.
        :param iv: O vetor de inicialização.
        :return: O conteúdo descriptografado do segmento.
        """
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key_content), modes.CBC(self.key_iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(content) + decryptor.finalize()

        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return decrypted_data
