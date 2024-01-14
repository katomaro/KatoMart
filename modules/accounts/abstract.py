"""Este módulo contém a classe abstrata Account, 
que representa um usuário de forma geral."""

import requests
import time
import json

from abc import ABC, abstractmethod

class Account(ABC):
    """Esta é uma classe abstrata que representa um usuário de forma geral.

    Seus métodos devem ser reescritos pelas classes filhas.

    Atributos:
        username (str): O nome de usuário ou e-mail da conta.
        password (str): A senha da conta.
        platform_id (str): A ID numérica de uma plataforma suportada.

    Methods:
        _login (Protegido/Interno): Realiza o login na conta.
        _check_session_exists (Protegido/Interno): Verifica uma sessão existe.
    """
    def __init__(self,
                 username: str='',
                 password: str='',
                 database_manager=None):
        
        self.LOGIN_URL = ''
        self.REFRESH_URL = ''
        self.PRODUCTS_URL = ''
        
        self.current_time = self.get_current_time()

        self.username = username
        self.password = password
        self.platform_id = 0
        self.is_valid = False
        self.validated_at = 0
        self.has_authenticated = False
        self.authenticated_at = 0
        self.auth_token = ''
        self.auth_token_expires_at = 0
        self.refresh_token = ''
        self.refresh_token_expires_at = 0
        self.other_data = ''

        self._database_manager = database_manager

        self.session = self._restart_session()

        self._check_session_exists()

    def get_current_time(self) -> int:
        """Retorna o tempo atual em segundos."""
        return int(time.time())
    
    def dump_json_data(self, data) -> str:
        """Retorna os dados da conta em formato JSON."""
        return json.dumps(data, indent=4, ensure_ascii=False)

    def _restart_session(self) -> requests.Session:
        """Inicia uma sessão limpa da biblioteca requests."""
        session = requests.Session()
        settings = self._database_manager.get_all_settings()
        # TODO: Implementar um sistema de escolha de User-Agent
        session.headers['User-Agent'] = settings[5]['value']
        return session

    def _check_session_exists(self) -> None:
        """Verifica se a sessão já existe."""
        # Não é por que você pode fazer, que você deve fazer.
        account_data = self._database_manager.check_account_session(self)
        self.auth_token = account_data['auth_token']
        self.auth_token_expires_at = account_data['auth_token_expires_at']
        self.refresh_token = account_data['refresh_token']
        self.refresh_token_expires_at = account_data['refresh_token_expires_at']
    
    @abstractmethod
    def _login(self):
        """Realiza o login na conta."""

    @abstractmethod
    def _get_account_products(self):
        """Retorna os produtos da conta."""
    
    @abstractmethod
    def _get_product_information(self):
        """Retorna as informações de um produto."""
