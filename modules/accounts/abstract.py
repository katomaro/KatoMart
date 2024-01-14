"""Este módulo contém a classe abstrata Account, 
que representa um usuário de forma geral."""

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
        self.other_data = {}

        self._database_manager = database_manager

        self._check_session_exists()

    def __str__(self):
        return f'''Conta: {self.username}; Senha: {self.password};
'plataforma: {self.platform_id}'''

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
