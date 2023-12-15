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
        self._conn = sqlite3.connect(self.main_database)
        self._cursor = self._conn.cursor()

        if self.__should_update_schema:
            self.__update_schema()

    def __update_schema(self):
        """Atualiza o schema do banco de dados, pelo mais atual."""
        with open(self.main_db_dir / 'main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            self._cursor.executescript(sql_commands)
        self._conn.commit()
        print('[DATABASE] Schema atualizado com sucesso.')
