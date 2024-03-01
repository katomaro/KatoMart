import sqlite3
from pathlib import Path

class DatabaseManager:
    """
    Gerencia a conexão com o banco de dados e operações relacionadas.
    """
    
    def __init__(self, db_path):
        """
        Inicializa a instância do gerenciador do banco de dados.

        :param db_path: Caminho para o arquivo do banco de dados.
        """
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        """
        Inicializa o banco de dados, criando-o se não existir.
        """
        if not Path(self.db_path).exists():
                self.create_schema()
                self.insert_starter_data()

    def get_connection(self):
        """
        Obtém uma conexão com o banco de dados.

        :return: Conexão com o banco de dados.
        """
        return sqlite3.connect(self.db_path)

    def create_schema(self):
        """
        Cria o esquema do banco de dados (tabelas, índices, etc.).
        """

        with self.get_connection() as conn, open('main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            conn.executescript(sql_commands)
        conn.commit()
    
    def insert_starter_data(self):
        """
        Insere dados iniciais no banco de dados.
        """
        with self.get_connection() as conn, open('data.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            conn.executescript(sql_commands)
        conn.commit()

    def execute_query(self, query, params=(), fetchone=False):
        """
        Executa uma consulta SQL no banco de dados.

        :param query: String da consulta SQL.
        :param params: Parâmetros para a consulta SQL.
        :param fetchone: Se deve buscar apenas um resultado.
        :return: Resultado da consulta.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            return result

if __name__ == "__main__":
    db_manager = DatabaseManager("main.sqlite3")
    db_manager.create_schema()
    db_manager.insert_starter_data()
