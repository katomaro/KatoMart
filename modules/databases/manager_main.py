"""Este módulo é responsável por gerenciar o banco de dados principal"""

import sqlite3

from os.path import abspath, dirname


class ManagerMain:
    """Esta classe é responsável por gerenciar o banco de dados principal."""
    def __init__(self):
        self.dir = dirname(abspath(__file__))
        self._conn = sqlite3.connect(self.dir + '/main.sqlite3')
        self._cursor = self._conn.cursor()
        if isinstance(self, ManagerMain):
            self.__update_schema()

    def __update_schema(self):
        """Atualiza o schema do banco de dados, pelo mais atual."""
        with open(self.dir + '/main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            self._cursor.executescript(sql_commands)
        self._conn.commit()
        print('[DATABASE] Schema atualizado com sucesso.')
