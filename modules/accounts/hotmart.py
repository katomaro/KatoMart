"""Código referente ao consumo de produtos da Hotmart"""

from .abstract import Account


class Hotmart(Account):
    """Esta é uma classe que representa um usuário da Hotmart."""
    def __init__(self,
                 username: str='',
                 password: str='',
                 database_manager=None):
        super().__init__(username=username, password=password, database_manager=database_manager)
        self.platform_id = 1
    
    def _login(self):
        """Realiza o login na conta."""
        print(self.username, self.auth_token, self.password, self.refresh_token, self.platform_id)
    
    def _get_account_products(self):
        """Retorna os produtos da conta."""
    
    def _get_product_information(self):
        """Retorna as informações de um produto."""
