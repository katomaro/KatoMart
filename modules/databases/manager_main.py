import sqlite3
from pathlib import Path

class DatabaseManager:
    """
    Gerencia a conexão com o banco de dados e operações relacionadas.
    """
    
    def __init__(self, db_folder_path: Path = '', db_path: Path = ''):
        """
        Inicializa a instância do gerenciador do banco de dados.

        :param db_folder_path: Caminho para a pasta do banco de dados.
        :param db_path: Caminho para o arquivo do banco de dados.
        """
        self.db_folder_path = db_folder_path
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

        with self.get_connection() as conn, open(self.db_folder_path / 'main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            conn.executescript(sql_commands)
        conn.commit()
    
    def insert_starter_data(self):
        """
        Insere dados iniciais no banco de dados.
        """
        with self.get_connection() as conn, open(self.db_folder_path / 'data.sql', 'r', encoding='utf-8') as sql_file:
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
    
    def get_all_settings(self):
        """
        Retorna todas as configurações do banco de dados.

        :return: Dicionário com todas as configurações.
        """
        query = "SELECT key, value FROM Settings"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            settings = {row[0]: row[1] for row in cursor.fetchall()}
        return settings
    
    def get_setting(self, key):
        """
        Retorna uma configuração do banco de dados.

        :param key: Chave da configuração.
        :return: Valor da configuração.
        """
        query = "SELECT value FROM Settings WHERE key = ?"
        return self.execute_query(query, (key,), fetchone=True)[0]

    def get_all_media_delivery_sources(self):
        """
        Retorna todas as fontes de entrega de mídia do banco de dados.

        :return: Lista com todas as fontes de entrega de mídia.
        """
        query = "SELECT name, description, download FROM MediaDeliverySources"
        return self.execute_query(query)

    def get_all_drm_types(self):
        """
        Retorna todos os tipos de DRM do banco de dados.

        :return: Lista com todos os tipos de DRM.
        """
        query = "SELECT name, description, download FROM DRMTypes"
        return self.execute_query(query)

    def update_setting(self, key, value):
        """
        Atualiza uma configuração no banco de dados.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Settings SET value = ? WHERE key = ?", (value, key))
            conn.commit()

if __name__ == "__main__":
    manager_path = Path(__file__).resolve().parent
    db_manager = DatabaseManager(manager_path, manager_path / 'main.sqlite3')
    db_manager.create_schema()
    db_manager.insert_starter_data()
