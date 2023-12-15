"""Este módulo é responsável por gerenciar o banco de dados principal"""

import sqlite3

from pathlib import Path
from typing import Tuple

from modules.accounts.abstract import Account


class ManagerMain:
    """Esta classe é responsável por gerenciar o banco de dados principal."""
    def __init__(self):
        self.main_db_dir = Path(__file__).parent
        self.main_database = self.main_db_dir / 'main.sqlite3'
        self.__should_update_schema = False
        if not self.main_database.exists():
            self.__should_update_schema = True
        self._main_conn = sqlite3.connect(self.main_database)
        self._main_conn.row_factory = sqlite3.Row

        if self.__should_update_schema:
            self.__update_schema()

    def __update_schema(self) -> None:
        """Atualiza o schema do banco de dados, pelo mais atual."""
        cursor = self._main_conn.cursor()
        with open(self.main_db_dir / 'main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            cursor.executescript(sql_commands)
        self._main_conn.commit()
        cursor.close()
        print('[DATABASE] Schema prncipal do banco de dados atualizado com sucesso.')
        self.__update_supported_platforms()

    def __update_supported_platforms(self) -> None:
        """Atualiza as plataformas suportadas pelo programa."""
        cursor = self._main_conn.cursor()
        with open(self.main_db_dir / 'supported_platforms.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            cursor.executescript(sql_commands)
        self._main_conn.commit()
        cursor.close()
        total = self._main_conn.execute('SELECT count(name) SELECT Platforms').fetchone()[0]
        print(f'[DATABASE] {total} Plataformas suportadas atualizadas com sucesso.')

    def get_supported_platforms(self) -> Tuple[sqlite3.Row, ...]:
        """Retorna as plataformas suportadas pelo programa."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT * from Platforms')
        platforms = cursor.fetchall()
        cursor.close()
        return platforms

    def insert_new_account(self, new_account: Account=Account('Invalida', '123', 1)) -> Account:
        """Insere uma nova conta no banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Accounts (username, password, platform_id) values (?, ?, ?)',
                       (new_account.username, new_account.password, new_account.platform_id))
        self._main_conn.commit()
        cursor.close()
        return new_account
