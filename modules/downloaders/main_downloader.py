import json
import os
import pathlib
import re
import shutil
import subprocess
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
        self.current_platform_id = self.account.get_platform_id()

        self.request_session: requests.Session = None
        self.create_download_session()

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


    def create_download_session(self):
        """
        Copia a sessão principal para ser manipulada pelo downloader.
        """
        self.request_session = self.account.clone_main_session()

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

    def get_courses_progress(self) -> list:
        """
        Retorna uma lista de dicionário com o progresso dos cursos.
        """
        pass

    def iter_account_contents(self):
        """
        Itera sobre os conteúdos de uma conta.
        """
        # Aqui a gente assume que o método da conta organizou todo o conteúdo, então não precisamos ir buscar informaçções
        # Pode vir ser necessário no futuro, então... TODO: Implementar um chamada para buscar informações precisas
        for content in self.account.downloadable_products:
            download_path = pathlib.Path(content.get('save_path'))
            content = content.get('data')
            content['progress'] = 0
            self.current_content_id = content['id']
            self.current_content_url = content['domain']
            self.current_content_name = content['name']
            self.current_content_progress = content['progress']
            download_path = download_path / remover_caracteres_problematicos(content['name'])
            if not download_path.exists():
                download_path.mkdir(parents=True)
            self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Download do curso {content['name']} iniciado para o caminho {download_path} ^-^")
            if not content.get('modules'):
                self.get_content_modules()
            for module in content.get('modules'):
                self.current_module_id = module['id']
                self.current_module_name = module['name']
                module_path = download_path / remover_caracteres_problematicos(f"{module['moduleOrder']}. " + module['name'])
                self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Listando conteúdos do módulo: {module_path} ^-^")
                if not module.get('lessons'):
                    self.get_content_lessons()
                for lesson in module.get('lessons'):
                    self.current_lesson_id = lesson['id']
                    self.current_lesson_name = lesson['name']
                    lesson_path = module_path / remover_caracteres_problematicos(f"{lesson['lessonOrder']}. " + lesson['name'])
                    self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Baixando a aula: {lesson_path} ^-^")
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
                            if not self.scan_html_for_videos:
                                self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Conteúdo textual salvo: {lesson_path}")
                            else:
                                self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Conteúdo textual salvo, como o scan por vídeos está ativado, o programa vai tentar procurar vídeos no conteúdo textual e salvar na pasta: {lesson_path}")
                                self.scan_text_content(lesson_files['text_content'], lesson_path)

                        if lesson_files.get('references'):
                            file_name = 'Referências.txt'
                            with open(lesson_path / file_name, 'w', encoding='utf-8') as f:
                                for reference in lesson_files['references']:
                                    f.write(f"{reference}\n")
                            self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Salvando referências: {lesson_path}")

                        if lesson_files.get('medias'):
                            for media_index, media in enumerate(lesson_files['medias'], start=1):
                                if self.use_original_media_name:
                                    media_name = f"{media_index}. {remover_caracteres_problematicos(media['name'])}"
                                    media_name = media_name.rsplit('.', 1)[0] + '.ts'
                                else:
                                    media_name = f"{media_index}. Aula.ts"
                                self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Baixando {len(lesson_files['medias'])} mídias, atual: {lesson_path}/{media['name']}")
                                self.download_content(media, lesson_path, media_name, is_attachment=False)

                        if lesson_files.get('attachments'):
                            temp_path = lesson_path / 'Anexos'
                            self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Esta aula possui anexos, tentando baixar para: {temp_path}")
                            for attachment_index, attachment in enumerate(lesson_files['attachments'], start=1):
                                if self.use_original_media_name:
                                    attachment_name = f"{attachment_index}. {attachment['name']}"
                                else:
                                    attachment_name = f"{attachment_index}. Anexo.{attachment['name'].split('.')[-1]}"
                                self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Baixando {len(lesson_files['attachments'])} anexos, atual: {lesson_path}/{attachment['name']}")
                                self.download_content(attachment, temp_path, attachment_name, is_attachment=True)
                                self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Anexo baixado com sucesso: {temp_path}/{attachment['name']}")
                            self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Ciclo de download de anexos da aula finalizado ^-^")
                        else:
                            self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Não foram encontrados anexos para a aula: {lesson_path}")
                    else:
                        self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data=f"Não foram encontrados materiais para a aula: {lesson_path}")

    def scan_text_content(self, text_content:str, save_path:pathlib.Path):
        """
        Procura por links de vídeo em um conteúdo textual.
        :param text_content: O conteúdo textual a ser analisado.
        :param save_path: O caminho para salvar os vídeos encontrados.
        """
        soup = BeautifulSoup(text_content, 'html.parser')
        found_videos = []
        # Procura por vídeos em tags de vídeo
        for video in soup.find_all('video'):
            video_url = video.get('src')
            found_videos.append(video_url)
        # Procura por vídeos em iFrames
        for iframe in soup.find_all('iframe'):
            iframe_url = iframe.get('src')
            found_videos.append(iframe_url)
        # Procura por vídeos em links
        for link in soup.find_all('a'):
            link_url = link.get('href')
            found_videos.append(link_url)
        # Procura por vídeos em texto  # Possivelmente melhor passar um regex inteiro em parágrafos? Mas existem outras tags de conteúdo textual...
        # for paragraph in soup.find_all('p'):
        #     paragraph_text = paragraph.get_text()
        #     if 'video' in paragraph_text.lower():
        #         self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Possível vídeo encontrado no conteúdo textual em um parágrafo: {paragraph_text}")
        # Procura por vídeos em scripts
        # for script in soup.find_all('script'):
        #     script_text = script.get_text()
        #     if 'video' in script_text.lower():
        #         self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Possível vídeo encontrado no conteúdo textual em um script: {script_text}")
        media_counter = 1
        if found_videos:
            self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Foram encontrados {len(found_videos)} possíveis vídeos no conteúdo textual, testando um a um e tentando baixar para: {save_path}")
            for video_url in found_videos:
                if self.resolve_linked_player(video_url, save_path, media_count=media_counter):
                    media_counter += 1
        else:
            self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data="Nenhum possível vídeo encontrado no conteúdo textual")

    def resolve_linked_player(self, video_url:str, save_path:pathlib.Path, media_count:int = 1) -> bool:
        """
        Resolve um player de vídeo e baixa o conteúdo pelo método correto.
        """
        # youtube.com, youtu.be, vimeo.com
        odio = r'(https?:)?//(?:www\.)?(youtube\.com/watch\?v=|youtu\.be/|vimeo\.com/\d+|player.vimeo.com/video/\d+)[\w-]*\??[\w=&]*'
        link = re.search(odio, video_url)
        if link:
            self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Vídeo encontrado: {link}")
            self.download_ytdlp_media(link.group(0), referer=self.current_content_url, save_path=save_path, media_index=media_count)
            return True
        return False

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
        self.download_path.mkdir(parents=True, exist_ok=True)
        self.file_name = file_name
        self.media_id = file.get('hash')
        self.media_size = file.get('size')
        self.media_duration_secs = file.get('duration')
        self.media_url = file.get('url')
        if file.get('is_stream'):
            self.get_video_playlist()
        else:
            self.download_raw_file(is_attachment=is_attachment)
        
        self.post_download()
    
    def post_download(self) -> None:
        """
        Pós processamento após o download.
        """
        if self.file_name.endswith('.ts'):
            self.ts_to_mp4(self.download_path / self.file_name)
        self.completed_files += 1
        self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Download de {self.file_name} concluído! ^-^")

    def get_video_playlist(self):
        """
        Baixa a playlist de vídeo m3u8.
        """
        is_stream = False
        has_drm = False
        data = {}
        self.request_session.headers['Referer'] = self.current_content_url

        response = self.request_session.get(self.media_url)
        if response.status_code != 200:
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=1, log_data=f"Erro ao baixar a playlist de vídeo: {self.media_url} - {self.current_content_name} - {self.current_module_name} - {self.current_lesson_name}")
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
                        with open(self.download_path / (self.file_name.rsplit('.', 1)[0] + f"_{subtitle.language}.vtt"), 'wb') as f:
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
            
            if playlist.version is not None and int(playlist.version) >= 4:
                self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Playlist de vídeo com versão {playlist.version}, pode gerar vídeos corrompidos!")

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
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=1, log_data=f"Erro ao baixar a playlist mestra: {playlist_url}")

        return response.text

    def handle_html_response(self, html_content:str) -> dict:
        """
        Lida com uma resposta HTML usando o BeautifulSoup.
        """
        filtered_html = {}
        soup = BeautifulSoup(html_content, 'html.parser')
        if self.current_platform_id == 1:
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

            content = self.download_with_retries()
            if content:
                with open(self.download_path / self.file_name, 'a+b') as f:
                    f.write(content)

    def download_encrypted_hls(self, playlist: m3u8.M3U8):
        """
        Baixa o arquivo m3u8 e os segmentos de vídeo criptografados.
        :param playlist: A playlist de vídeo m3u8.
        """
        if playlist.keys:
            for key in playlist.keys:
                if key:  # Se existir uma chave na playlist
                    key_uri = key.uri
                    if not key_uri.startswith('http'):
                        self.key_content = self.request_session.get(self.current_base_playlist_url + self.selected_quality_url.split('/', 1)[0] + '/' + key_uri).content  # Baixa a chave de encriptação
                    else:
                        self.key_content = self.request_session.get(key_uri).content
                    
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

                content = self.download_with_retries(segment_url)
                if content and self.key_content:
                    content = self.decrypt_segment(content)
                    with open(self.download_path / self.file_name, 'a+b') as f:
                        f.write(content)

    def download_raw_file(self, is_attachment:bool=False):
        """
        Baixa um arquivo diretamente.
        """
        if self.current_platform_id == 1 and is_attachment:
            self.download_hotmart_media()

    def download_hotmart_media(self):
        """
        Baixa um arquivo de mídia do Hotmart.
        """
        self.account.database_manager.log_event(log_type='INFO', sensitive_data=0, log_data=f"Baixando anexo da hotmart: {self.current_content_name} - {self.current_module_name} - {self.current_lesson_name} - {self.file_name} ^-^ {self.media_size} bytes")
        file_hash = self.media_id
        file_name = self.file_name
        file_info = self.download_with_retries(f"{self.account.MEMBER_AREA_URL.rsplit('/', 1)[0]}/attachment/{file_hash}/download?attachmentId={file_hash}")
        if not file_info:
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data=f"Erro ao baixar o arquivo {file_name}, pulando para o próximo arquivo!")
            return
        file_info = json.load(file_info)

        if file_info.get('directDownloadUrl'):
            url = file_info['directDownloadUrl']

            file_data = self.download_with_retries(url)
            if not file_data:
                self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data=f"Erro ao baixar o arquivo {file_name}, ele usa um link direto e não foi possível baixar, pulando para o próximo arquivo!")
                return
            with open(self.download_path / file_name, 'wb') as f:
                f.write(file_data.content)
        # aws
        elif file_info.get('lambdaUrl'):
            temp_session = self.account.clone_main_session()
            temp_session.headers['authority'] = 'drm-protection.cb.hotmart.com'
            temp_session.headers['token'] = file_info.get('token')
            url = temp_session.get('https://drm-protection.cb.hotmart.com').text
            file_data = requests.get(url)
            with open(self.download_path / file_name, 'wb') as f:
                f.write(file_data.content)
            self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Download de {file_name} concluído! Ele precisará de uma senha para ser aberto (provavelmente seu email da hotmart) ^-^")
    
    def download_ytdlp_media(self, url:str, referer:str=None, save_path:str=None, media_index:int=1):
        """
        Baixa um vídeo ou playlist de vídeos do YouTube usando yt-dlp.
        :param url: URL do vídeo ou playlist a ser baixado pelo yt-dlp.
        :param referer: URL de referência para o download.
        :param save_path: Caminho para salvar o arquivo.
        :param media_index: Índice da mídia a ser salva.
        """
        ytdlp_opts = {
            'retries': 8,
            'fragment_retries': 6,
            'concurrent_fragment_downloads': int(self.download_threads),
            'outtmpl': save_path.as_posix() + f'/{media_index}. ' + '%(title)s.%(ext)s',}
        with yt_dlp.YoutubeDL(ytdlp_opts) as ytdlp:
            if referer:
                ytdlp.params['http_headers'] = {'Referer': referer}
            ytdlp.download([url])
        self.account.database_manager.log_event(log_type='SUCCESS', sensitive_data=0, log_data=f"Download de {url} concluído! ^-^")

    def download_widevine_media(self, url:str, save_path:str):
        """
        Baixa um vídeo protegido por Widevine.
        """
        raise NotImplementedError

    def download_with_retries(self, file_url:str = '',
                              use_raw_session: bool = False,
                              clone_main_session: bool = False,
                              use_specific_session: bool = False,
                              specific_session: requests.Session = None) -> bytes | None:
        """
        Tenta baixar um arquivo com o número de retentativas configurado no painel.
        
        :param file_url: URL do segmento a ser baixado.
        :param use_raw_session: Se a sessão de download deve ser a sessão principal ou uma sessão 'crua'.
        :param clone_main_session: Se a sessão de download deve ser clonada da sessão principal.
        :param use_specific_session: Se a sessão de download deve ser uma sessão específica.
        :param specific_session: A sessão específica a ser usada para o download.

        :return: O conteúdo do arquivo em bytes, se o download for bem-sucedido; None, caso contrário.
        """
        ephemereal_session = None

        for attempt in range(self.download_retries):
            try:
                if not use_raw_session and not use_specific_session:
                    response = self.request_session.get(file_url,
                                                        timeout=self.download_timeout)
                elif use_specific_session:
                    ephemereal_session = specific_session
                elif clone_main_session:
                    ephemereal_session = self.account.clone_main_session()
                else:
                    ephemereal_session = requests.Session()
                    ephemereal_session.headers['user-agent'] = self.request_session.headers['user-agent']
                    ephemereal_session.headers['referer'] = self.request_session.headers['referer']
                
                response = ephemereal_session.get(file_url,
                                        timeout=self.download_timeout)
                
                response.raise_for_status()
                
                return response.content
            
            except requests.RequestException as e:
                self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data=f"Erro ao baixar falha ao baixar o arquivo, tentativa {attempt + 1} de {self.download_retries}. Erro: {e}")
                time.sleep(self.download_timeout)

        self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data=f"Erro ao baixar o arquivo {file_url} após {self.download_retries} tentativas, prosseguindo")

        return None
    
    def recreate_session(self):
        """
        Recria a sessão de download a partir da conta.
        """
        raise NotImplementedError

    def decrypt_segment(self, content:bytes) -> bytes:
        """
        Descriptografa um segmento de mídia usando AES.
        
        :param content: O conteúdo criptografado do segmento.
        :return: O conteúdo descriptografado do segmento.
        """
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key_content), modes.CBC(self.key_iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(content) + decryptor.finalize()

        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return decrypted_data
    
    def ts_to_mp4(self, input_file: pathlib.Path) -> None:
        """
        Transforma a junção de segmentos ts para um arquivo mp4.
        
        :param input_file: O arquivo ts a ser transformado em mp4.
        """
        output_file = input_file.with_suffix('.mp4')
        self.account.database_manager.log_event(log_type='WARNING', sensitive_data=0, log_data=f"Convertendo {input_file} para {output_file}")
        ffmpeg_path = None
        if not self.use_custom_ffmpeg:
            ffmpeg_path = shutil.which('ffmpeg')
        if self.use_custom_ffmpeg:
            ffmpeg_path = self.custom_ffmpeg_path
        if not ffmpeg_path:
            self.account.database_manager.log_event(log_type='ERROR', sensitive_data=0, log_data="FFMPEG não encontrado, abortando conversão de ts para mp4!")
            return
        subprocess.run([ffmpeg_path, '-i', input_file, '-c', 'copy', output_file], check=True)
        input_file.unlink()
