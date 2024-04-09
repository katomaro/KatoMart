import json
import time

import m3u8
import requests
import yt_dlp

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from modules.accounts.abstract import Account
from modules.databases.manager_main import DatabaseManager



# TODO: Refatorar todos os requests para usar a sessão da conta
# TODO: Alterar os prints para um database.log ou um logger

def download_segment(segment_url:str = '', max_retries:int=5, delay_between_retries:int=3):
    """
    Tenta baixar um segmento com um determinado número de retentativas.
    
    :param segment_url: URL do segmento a ser baixado.
    :param max_retries: Número máximo de retentativas.
    :param delay_between_retries: Tempo de espera entre retentativas, em segundos.
    :return: O conteúdo do segmento, se o download for bem-sucedido; None, caso contrário.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(segment_url, stream=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Erro ao baixar {segment_url}, tentativa {attempt + 1} de {max_retries}. Erro: {e}")
            time.sleep(delay_between_retries)
    print(f"[DOWNLOADER] Falha ao baixar o segmento após {max_retries} tentativas: {segment_url}")
    return None


def decrypt_segment(content, key, iv):
    """
    Descriptografa um segmento de mídia usando AES.
    
    :param content: O conteúdo criptografado do segmento.
    :param key: A chave de criptografia.
    :param iv: O vetor de inicialização.
    :return: O conteúdo descriptografado do segmento.
    """
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(content) + decryptor.finalize()


class Downloader:
    def __init__(self, account: Account=None, database_manager: DatabaseManager=None) -> None:
        self.account = account
        self.database_manager = database_manager

        self.url_download = None
        self.download_path = None
        self.file_name = None


    def iter_account_contents(self):
        """
        Itera sobre os conteúdos de uma conta.
        """
        # TODO: Iterar pelo self.account.downloadable_products
        pass
    
    def download_content(self, url_download:str, download_path:str, file_name:str):
        """
        Baixa um conteúdo de uma URL.
        """
        self.url_download = url_download
        self.download_path = download_path
        self.file_name = file_name

        if self.url_download.endswith('.m3u8'):
            self.get_video_playlist()
        else:
            self.download_raw_file()

    def get_video_playlist(self):
        """
        Baixa a playlist de vídeo m3u8.
        """
        response = requests.get(self.url_download)
        if response.status_code == 200:
            playlist = m3u8.loads(response.text)
            if playlist.keys:
                self.download_encrypted_hls(playlist)
            else:
                self.download_raw_hls(playlist)
        return None

    def download_raw_hls(self, playlist: m3u8.M3U8):
        """
        Baixa o arquivo m3u8 e os segmentos de vídeo.
        """
        output_video_file = self.download_path + self.file_name + '.ts'

        with open(output_video_file, 'wb') as f:
            for segment in playlist.segments:

                segment_url = segment.uri
                if not segment_url.startswith('http'):
                    segment_url = '/'.join(self.url_download.split('/')[:-1]) + '/' + segment.uri

                content = download_segment(segment_url)
                if content:
                    f.write(content)
                else:
                    print(f"[DOWNLOADER]Não foi possível baixar o segmento: {segment_url}. Continuando para o próximo.")

    def download_encrypted_hls(self, playlist: m3u8.M3U8):
        """
        Baixa o arquivo m3u8 e os segmentos de vídeo criptografados.
        """
        output_video_file = self.download_path + self.file_name + '.ts'

        if playlist.keys:
            for key in playlist.keys:
                if key:  # Se existir uma chave na playlist
                    key_uri = key.uri
                    key_content = requests.get(key_uri).content  # Baixa a chave de encriptação
                    iv = key.iv  # Pode ser None, neste caso você pode querer gerar um IV baseado no número do segmento ou usar um IV padrão
                    if iv:
                        iv = bytes.fromhex(iv[2:])  # Remove o prefixo '0x' e converte para bytes
                    else:
                        # Aqui você precisaria definir um IV padrão ou gerar um baseado no segmento
                        iv = b'\x00' * 16  # Exemplo de IV padrão
                    break  # Este exemplo assume apenas uma chave para todos os segmentos

        with open(output_video_file, 'wb') as f:
            for segment in playlist.segments:
                segment_url = segment.uri
                if not segment_url.startswith('http'):
                    segment_url = '/'.join(self.url_download.split('/')[:-1]) + '/' + segment.uri

                content = download_segment(segment_url)
                if content and key_content:
                    content = decrypt_segment(content, key_content, iv)
                if content:
                    f.write(content)
                else:
                    print(f"Não foi possível baixar ou descriptografar o segmento: {segment_url}. Continuando para o próximo.")
    
    def download_raw_file(self):
        """
        Baixa um arquivo diretamente.
        """
        response = requests.get(self.url_download)
        if response.status_code == 200:
            with open(self.download_path + self.file_name, 'wb') as f:
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
