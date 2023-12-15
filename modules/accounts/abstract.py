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
                 platform_id: int=0):
        self.username = username
        self.password = password
        self.platform_id = platform_id
        self._check_session_exists()

    def __str__(self):
        return f'''Conta: {self.username}; Senha: {self.password};
'plataforma: {self.platform_id}'''

    @abstractmethod
    def _login(self):
        """Realiza o login na conta.""" 

    def _check_session_exists(self) -> None:
        """Verifica se a sessão já existe."""
        raise NotImplementedError('Método ainda não implementado por ausência '
                                  'do controlador de db.')
        # return self._login()
