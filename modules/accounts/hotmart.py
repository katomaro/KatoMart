"""Código referente ao consumo de produtos da Hotmart"""

from .abstract import Account

class Hotmart(Account):
    """
    Representa um usuário da Hotmart, especializando a classe Account para
    lidar com as especificidades desta plataforma.
    """
    
    def __init__(self, username: str='', password: str='', database_manager=None):
        """
        Inicializa uma instância de Hotmart.

        :param username: Nome de usuário ou e-mail.
        :param password: Senha da conta.
        :param database_manager: Gerenciador de banco de dados para esta conta.
        """
        super().__init__(username=username, password=password, database_manager=database_manager)
        self.platform_id = self.get_platform_id()
        self.LOGIN_URL = 'https://sec-proxy-content-distribution.hotmart.com/club/security/oauth/token'
        

    def get_platform_id(self):
        """
        Retorna o ID da plataforma de cursos.
        """
        platform_id = self._database_manager.execute_query(
            'SELECT id FROM platforms WHERE name = ? LIMIT 1', 
            ('Hotmart',), 
            fetchone=True
            )
        return platform_id

    def login(self):
        """
        Realiza o login na conta da Hotmart, autenticando o usuário e obtendo tokens de acesso.
        """
        raise NotImplementedError("Método não implementado.")

    def get_account_products(self):
        """
        Retorna os produtos associados à conta do usuário na Hotmart.
        """
        raise NotImplementedError("Método não implementado.")

    def get_product_information(self, product_id):
        """
        Retorna informações de um produto específico associado à conta do usuário.
        """
        raise NotImplementedError("Método não implementado.")
