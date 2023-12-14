"""Este módulo contém a classe abstrata Account, 
que representa um usuário de forma geral."""

from abc import ABC, abstractmethod

class Account(ABC):
    """Esta é uma classe abstrata que representa um usuário de forma geral.

    Seus métodos devem ser reescritos pelas classes filhas.

    Atributos:
        username (str): O nome de usuário ou e-mail da conta.
        password (str): A senha da conta.
        token (str): O token de acesso da conta, caso já exista uma sessão.
        token_creation (int): A data de criação do token em EPOCH (segundos).
        token_exp (int): A data de expiração do token em EPOCH (segundos).

    Methods:
        login: Realiza o login na conta.
        method2: Brief description of method2.
    """
    def __init__(self,
                 username: str='',
                 password:str='',
                 token:str='',
                 token_creation:int=0,
                 token_exp:int=0):
        self.username = username
        self.password = password
        self.token = token
        self.token_creation = token_creation
        self.token_exp = token_exp


    @abstractmethod
    def login(self):
        """Realiza o login na conta."""   


    def __str__(self):
        return '''Conta: {self.username}; Senha: {self.password};
'Token: {self.token}; Data de criação do token: {self.token_creation};
'Data de expiração do token: {self.token_exp}'''
