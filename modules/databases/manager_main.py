import sqlite3
from pathlib import Path
import time


class DatabaseManager:
    """
    Gerencia a conexão com o banco de dados e operações relacionadas.
    """
    
    def __init__(self, db_folder_path: Path = Path(''), db_path: Path = Path('')):
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
            settings = {
                row[0]: (
                    row[1]
                    if not str(row[1]) in ("0", "1")
                    else row[1] in ("1", 1)
                )
                for row in cursor.fetchall()
            }
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
        result = self.execute_query(query)
        return [{"name": row[0], "description": row[1], "download": bool(row[2])} for row in result]

    def update_media_delivery_source_download(self, name, download):
        """
        Atualiza o campo `download` de uma fonte de entrega de mídia.

        `download` indica se bot deve baixar o conteúdo desta fonte ou não.
        """
        query = "UPDATE MediaDeliverySources SET download = ? WHERE name = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (download, name))
            conn.commit()

    def get_all_drm_types(self):
        """
        Retorna todos os tipos de DRM do banco de dados.

        :return: Lista com todos os tipos de DRM.
        """
        query = "SELECT name, description, download FROM DRMTypes"
        result = self.execute_query(query)
        return [{"name": row[0], "description": row[1], "download": bool(row[2])} for row in result]

    def update_drm_type_download(self, name, download):
        """
        Atualiza o campo `download` de um tipo de DRM.

        `download` indica se bot deve baixar o conteúdo deste tipo de DRM ou não.
        """
        query = "UPDATE DRMTypes SET download = ? WHERE name = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (download, name))
            conn.commit()
    
    def get_all_media_types(self):
        """
        Retorna todos os tipos de DRM do banco de dados.

        :return: Lista com todos os tipos de DRM.
        """
        query = "SELECT name, description, download FROM MediaTypes"
        result = self.execute_query(query)
        return [{"name": row[0], "description": row[1], "download": bool(row[2])} for row in result]

    def update_media_type_download(self, name, download):
        """
        Atualiza o campo `download` de um tipo de mídia.

        `download` indica se bot deve baixar este tipo de mídia ou não.
        """
        query = "UPDATE MediaTypes SET download = ? WHERE name = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (download, name))
            conn.commit()

    def update_setting(self, key, value):
        """
        Atualiza uma configuração no banco de dados.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Settings SET value = ? WHERE key = ?", (value, key))
            conn.commit()
    
    def fetch_platforms(self):
        """
        Retorna todas as plataformas do banco de dados.

        :return: Lista com todas as plataformas.
        """
        query = "SELECT id, name FROM Platforms"
        return self.execute_query(query)
    
    def add_or_update_account(self, platform_id, email, password, added_at, last_validated_at, is_valid):
        with self.get_connection() as conn:
            is_valid_int = 1 if is_valid else 0
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM Accounts WHERE username = ? AND platform_id = ?", (email, platform_id))
            account = cursor.fetchone()

            if account:
                cursor.execute("UPDATE Accounts SET password = ?, added_at = ?, is_valid = ?, last_validated_at = ? WHERE id = ?",
                            (password, added_at, is_valid_int, last_validated_at, account[0]))
            else:
                cursor.execute("INSERT INTO Accounts (username, password, added_at, is_valid, last_validated_at, platform_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (email, password, added_at, is_valid_int, last_validated_at, platform_id))

        conn.commit()
    
    def update_auth_token(self, account_id, platform_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data):
        with self.get_connection() as conn:
            cursor = conn.cursor()

        cursor.execute("SELECT id FROM Auths WHERE account_id = ? AND platform_id = ?", (account_id, platform_id))
        auth = cursor.fetchone()
        if auth:
            # Atualizar o token existente
            cursor.execute("""
                UPDATE Auths
                SET auth_token = ?, auth_token_expires_at = ?, refresh_token = ?, refresh_token_expires_at = ?, other_data = ?
                WHERE id = ?
            """, (auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data, auth[0]))
        else:
            # Inserir um novo token
            cursor.execute("""
                INSERT INTO Auths (account_id, platform_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (account_id, platform_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data))

        conn.commit()
    
    def get_session_token_by_email(self, platform_id, email):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Primeiro, encontre o account_id correspondente ao email e platform_id fornecidos
            cursor.execute("""
                SELECT a.id FROM Accounts a
                WHERE a.username = ? AND a.platform_id = ?
            """, (email, platform_id))
            account_result = cursor.fetchone()

            if account_result:
                account_id = account_result[0]

                cursor.execute("""
                    SELECT auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data
                    FROM Auths
                    WHERE account_id = ? AND platform_id = ?
                """, (account_id, platform_id))
                token_info = cursor.fetchone()

                if token_info:
                    # Convertendo a tupla em um dicionário para facilitar pq o pai n ta tankando nkkkkkkkkkkk
                    keys = ["auth_token", "auth_token_expires_at", "refresh_token", "refresh_token_expires_at", "other_data"]
                    return dict(zip(keys, token_info))
                else:
                    return None
            else:
                return None
    
    def get_accounts_by_platform(self, platform_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Assumindo que 'Accounts' tenha uma coluna 'platform_id' que relaciona com 'Platforms'
            query = '''
            SELECT id, username, platform_id, password, is_valid FROM Accounts
            WHERE platform_id = ?
            '''
            cursor.execute(query, (platform_id,))
            accounts = [{"id": row[0], 
                         "username": row[1], 
                         "platform_id": row[2], 
                         "password": row[3], 
                         "is_valid": row[4], } for row in cursor.fetchall()]
            
            for account in accounts:
                cursor.execute("SELECT auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data FROM Auths WHERE account_id = ?", (account['id'],))
                auth = cursor.fetchone()
                if auth:
                    account['auth_token'] = auth[0]
                    account['auth_token_expires_at'] = auth[1]
                    account['refresh_token'] = auth[2]
                    account['refresh_token_expires_at'] = auth[3]
                    account['other_data'] = auth[4]
                else:
                    account['auth_token'] = None
                    account['auth_token_expires_at'] = None
                    account['refresh_token'] = None
                    account['refresh_token_expires_at'] = None
                    account['other_data'] = None

            return accounts
    
    def delete_account(self, account_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Accounts WHERE id = ?", (account_id,))
            conn.commit()

    def log_event(self, log_type:str='WARN', sensitive_data:int=1, log_data: str='', log_created_at: int=0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if log_created_at == 0:
                log_created_at = int(time.time())

            cursor.execute("INSERT INTO Events (type, data) VALUES (?, ?)", (log_type, sensitive_data, log_data, log_created_at))
            conn.commit()
    
    # TODO: Implementar função de log paginado


if __name__ == "__main__":
    manager_path = Path(__file__).resolve().parent
    db_manager = DatabaseManager(manager_path, manager_path / 'main.sqlite3')
    db_manager.create_schema()
    db_manager.insert_starter_data()
