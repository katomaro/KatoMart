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

        # TODO: Implementar login por SSO, essa URL é antiga e está deprecada
        self.LOGIN_URL = 'https://sec-proxy-content-distribution.hotmart.com/club/security/oauth/token'
        self.PRODUCTS_URL = ''
    
    def _login(self):
        """Realiza o login na conta."""
        login_data = self.session.post(self.LOGIN_URL, data={
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
            }
        ).json()
        if 'error' in login_data:
            # TODO Passar o erro corretamente para o front-end posteriormente
            raise Exception(login_data['error_description'])
        
        self.is_valid = True
        self.validated_at = self.get_current_time()
        self.has_authenticated = True
        self.authenticated_at = self.get_current_time()
        self.auth_token = login_data['access_token']
        self.auth_token_expires_at = login_data['expires_in'] + self.get_current_time()
        self.refresh_token = login_data['refresh_token']
        self.other_data = {
            'scope': login_data['scope'],
            'token_type': login_data['token_type'],
            'jti': login_data['jti']
        }
    
    def _get_account_products(self):
        """Retorna os produtos da conta."""
    
    def _get_product_information(self):
        """Retorna as informações de um produto."""
