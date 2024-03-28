"""Código referente ao consumo de produtos da Hotmart"""

from .abstract import Account

class Hotmart(Account):
    """
    Representa um usuário da Hotmart, especializando a classe Account para
    lidar com as especificidades desta plataforma.
    """
    
    def __init__(self, account_id: int = 0, database_manager=None):
        """
        Inicializa uma instância de Hotmart.

        :param username: Nome de usuário ou e-mail.
        :param password: Senha da conta.
        :param database_manager: Gerenciador de banco de dados para esta conta.
        """
        super().__init__(account_id=account_id, database_manager=database_manager)
        self.platform_id = self.get_platform_id()
        # Estas URLs estão para mudar!
        self.LOGIN_URL = 'https://sec-proxy-content-distribution.hotmart.com/club/security/oauth/token'
        self.PRODUCTS_URL = 'https://sec-proxy-content-distribution.hotmart.com/club/security/oauth/check_token'
        self.MEMBER_AREA_URL = 'https://api-club.cb.hotmart.com/rest/v3/navigation'

        self.load_account_information()
        self.load_tokens()
        self.login()
        

    def get_platform_id(self):
        """
        Retorna o ID da plataforma de cursos.
        """
        platform_id = self._database_manager.execute_query(
            'SELECT id FROM platforms WHERE name = ? LIMIT 1', 
            ('Hotmart',), 
            fetchone=True
            )
        return platform_id[0]

    def login(self):
        """
        Realiza o login na conta da Hotmart, autenticando o usuário e obtendo tokens de acesso.
        """
        if not self.auth_token or self.auth_token_expires_at < self.get_current_time():
            login_data = {
                'grant_type': 'password',
                'username': self.username,
                'password': self.password
            }
            response = self.session.post(self.LOGIN_URL, data=login_data)

            if response.status_code != 200:
                raise Exception(f'Erro ao acessar {response.url}: Status Code {response.status_code}')

            response = response.json()
            self.auth_token = response['access_token']
            self.auth_token_expires_at = self.get_current_time() + response['expires_in']
            self.refresh_token = response['refresh_token']
            self.refresh_token_expires_at = self.get_current_time() + response['expires_in']
            self.other_data = self.dump_json_data(response)
            self._database_manager.execute_query("""
                INSERT OR REPLACE INTO Auths (account_id, platform_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.account_id, self.platform_id, self.auth_token, self.auth_token_expires_at, self.refresh_token, self.refresh_token_expires_at, self.other_data)
            )


    def get_account_products(self):
        """
        Retorna os produtos associados à conta do usuário na Hotmart.
        """
        data = {
            'token': self.auth_token
        }
        response = self.session.get(self.PRODUCTS_URL, params=data)
        if response.status_code != 200:
            raise Exception(f'Erro ao acessar {response.url}: Status Code {response.status_code}')
        response = response.json()['resources']
        products = []
        for resource in response:
            if resource.get('type') == 'PRODUCT':
                product_dict = {
                    'id': int(resource.get('resource', {}).get('productId')),
                    'subdomain': resource.get('resource', {}).get('subdomain'),
                    'status': resource.get('resource', {}).get('status'),
                    'user_area_id': int(resource.get('resource', {}).get('userAreaId')),
                    'roles': resource.get('roles'),
                    'domain': f"https://{resource.get('resource', {}).get('subdomain')}.club.hotmart.com"
                }
                products.append(product_dict)
        return products


    def get_product_information(self, club_name: str):
        """
        Retorna informações de um produto específico associado à conta do usuário.
        :club_name: nome da área de membros da htm.

        :return: Dicionário com informações do produto.
        """
        self.session.headers['authorization'] = f'Bearer {self.auth_token}'
        self.session.headers['club'] = club_name
        response = self.session.get(self.MEMBER_AREA_URL)
        if response.status_code != 200:
            raise Exception(f'Erro ao acessar {response.url}: Status Code {response.status_code}')
        return response.json()
