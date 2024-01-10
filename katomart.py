"""Ponto de inicialização para um futuro server Flask"""

from modules.databases.manager_main import ManagerMain
from modules.accounts.hotmart import Hotmart

if __name__ == '__main__':
    manager = ManagerMain()
    # print(manager.get_supported_platforms())
    account = Hotmart('teste', 'teste', database_manager=manager)
    account._login()
    # a = manager.insert_new_account(account)
    # print(a)

    print("Goodbye World! Alprazolam 2mg é bom. Lembre-se que você deve ser acompanhado por um médico.")
