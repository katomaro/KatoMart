from abc import ABC, abstractmethod

import pathlib
import os
import time
import json
import requests

from modules.databases.manager_main import DatabaseManager


class Account(ABC):
    """
    Classe abstrata que representa uma conta genérica e gerencia a sessão de autenticação.

    Atributos e métodos desta classe devem ser estendidos por classes específicas
    de plataformas de cursos.
    """

    def __init__(self, account_id: int = 0, database_manager: DatabaseManager = None):
        self.account_id = account_id
        self.username = ''
        self.password = ''
        self.is_valid = False
        self.validated_at = 0
        self.has_authenticated = False
        self.authenticated_at = 0
        self.auth_token = ''
        self.auth_token_expires_at = 0
        self.refresh_token = ''
        self.refresh_token_expires_at = 0
        self.other_data = ''
        self.database_manager = database_manager
        self.session = self._restart_requests_session()

        self.downloadable_products = []

    def _restart_requests_session(self) -> requests.Session:
        """
        Inicia uma sessão limpa da biblioteca requests.

        :return: Sessão da biblioteca requests com o User-Agent configurado.
        """
        session = requests.Session()
        settings = self.database_manager.get_all_settings()
        session.headers['User-Agent'] = settings.get('default_user_agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0')
        return session
    
    def get_current_time(self) -> int:
        """
        Retorna o tempo atual em segundos.
        """
        return int(time.time())

    def dump_json_data(self, data) -> str:
        """
        Serializa dados da conta em formato JSON.
        """
        return json.dumps(data, indent=4, ensure_ascii=False)

    def load_account_information(self) -> None:
        """
        Configura os atributos da conta com informações do banco de dados.
        """
        data = self.database_manager.execute_query("""
            SELECT username, password, added_at, is_valid, last_validated_at FROM Accounts WHERE id = ?""",
            (self.account_id,), fetchone=True)
        self.username = data[0]
        self.password = data[1]
        self.is_valid = bool(data[3])
        self.validated_at = data[4]
    
    def load_tokens(self) -> None:
        """
        Carrega os tokens de autenticação da conta.
        """
        data = self.database_manager.execute_query("""
            SELECT auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data
            FROM Auths WHERE account_id = ? AND platform_id = ?""",
            (self.account_id, self.get_platform_id()), fetchone=True)
        if data:
            self.auth_token = data[0]
            self.auth_token_expires_at = data[1]
            self.refresh_token = data[2]
            self.refresh_token_expires_at = data[3]
            self.other_data = data[4]
    
    def clone_main_session(self) -> requests.Session:
        """
        Clona a sessão principal da conta para uso temporário em requisições
        que podem mudar dados da sessão principal.
        """
        ephemereal_session = requests.Session()
        ephemereal_session.headers = self.session.headers.copy()
        ephemereal_session.cookies = requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies})
        ephemereal_session.auth = self.session.auth
        ephemereal_session.proxies = self.session.proxies.copy()
        ephemereal_session.hooks = self.session.hooks.copy()
        ephemereal_session.verify = self.session.verify

        return ephemereal_session
    
    def get_save_path(self) -> str:
        """
        Retorna o caminho de salvamento dos arquivos baixados.
        """
        settings = self.database_manager.get_all_settings()
        download_path = settings.get('download_path', 'downloads')
        download_path = pathlib.Path(os.path.abspath(__file__)).parent / download_path

        return str(download_path.resolve())
    
    @abstractmethod
    def get_platform_id(self) -> int:
        """
        Retorna o ID da plataforma de cursos.
        """

    @abstractmethod
    def login(self):
        """
        Método abstrato para realizar o login na plataforma.
        """

    @abstractmethod
    def refresh_auth_token(self):
        """
        Método abstrato para renovar o token de acesso.
        """

    @abstractmethod
    def get_account_products(self, get_extra_info: int = 0):
        """
        Método abstrato para obter os produtos associados à conta.
        """

    @abstractmethod
    def format_account_products(self, product_id: int | str | None = None, product_info: dict = None):
        """
        Método abstrato para formatar um produto ao padrão Módulo/Aula/Arquivos
        """

    @abstractmethod
    def format_product_information(self, product_info: dict):
        """
        Método abstrato para formatar as informações de um produto específico.
        """

    @abstractmethod
    def get_product_information(self, product_id : str | int):
        """
        Método abstrato para obter informações de um produto específico.
        """

    @abstractmethod
    def download_content(self, product_info: dict = None):
        """
        Método abstrato para baixar o conteúdo de um produto.
        cada plataforma pode requerer um pré-processamento diferente.
        """
