"""Este módulo é responsável por gerenciar o banco de dados principal"""

import sqlite3

from pathlib import Path


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

    def __update_schema(self):
        """Atualiza o schema do banco de dados, pelo mais atual."""
        cursor = self._main_conn.cursor()
        with open(self.main_db_dir / 'main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            cursor.executescript(sql_commands)
        self._main_conn.commit()
        cursor.close()
        print('[DATABASE] Schema prncipal do banco de dados atualizado com sucesso.')
        self.__update_supported_platforms()

    def __update_supported_platforms(self):
        """Atualiza as plataformas suportadas pelo programa."""
        cursor = self._main_conn.cursor()
        with open(self.main_db_dir / 'supported_platforms.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            cursor.executescript(sql_commands)
        self._main_conn.commit()
        cursor.close()
        total = self._main_conn.execute('select count(name) from Platforms').fetchone()[0]
        print(f'[DATABASE] {total} Plataformas suportadas atualizadas com sucesso.')
