"""Este módulo é responsável por gerenciar o banco de dados principal"""

import time
import sqlite3
import sys

from typing import Tuple
from pathlib import Path

from modules.accounts.abstract import Account


class ManagerMain:
    """Esta classe é responsável por gerenciar o banco de dados principal."""
    def __init__(self):
        self.start_time = int(time.time())
        self.main_db_dir = Path(__file__).parent
        self.main_database = self.main_db_dir / 'main.sqlite3'
        self.__should_update_schema = False
        if not self.main_database.exists():
            self.__should_update_schema = True
        self._main_conn = sqlite3.connect(self.main_database)
        self._main_conn.row_factory = sqlite3.Row

        if self.__should_update_schema:
            self.__update_schema()

    def __set_database_defaults(self) -> None:
        """Insere os valores padrões no banco de dados principal."""
        cursor = self._main_conn.cursor()
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('database_instanced_at', self.start_time))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('last_executed_at', self.start_time))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('user_consent', '0'))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('download_path', './Cursos/'))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('user_os', sys.platform))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('default_user_agent',
                                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'))
        
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('use_custom_ffmpeg', '0'))
        cursor.execute('INSERT INTO Settings(key, value) VALUES (?, ?)', ('custom_ffmpeg_path', 'SYSTEM'))
        self._main_conn.commit()
        cursor.close()

    def __update_schema(self) -> None:
        """Atualiza o schema do banco de dados, pelo mais atual."""
        cursor = self._main_conn.cursor()
        with open(self.main_db_dir / 'main.sql', 'r', encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
            cursor.executescript(sql_commands)
        self._main_conn.commit()

        self.__set_database_defaults()
        
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
        total = self._main_conn.execute('SELECT count(name) FROM Platforms').fetchone()[0]
        print(f'[DATABASE] {total} Plataformas suportadas atualizadas com sucesso.')

    def get_supported_platforms(self) -> Tuple[sqlite3.Row, ...]:
        """Retorna as plataformas suportadas pelo programa."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT * from Platforms')
        platforms = cursor.fetchall()
        cursor.close()
        return platforms

    def insert_new_account(self, new_account: Account=Account) -> None:
        """Insere uma nova conta no banco de dados."""
        cursor = self._main_conn.cursor()

        cursor.execute('INSERT OR UPDATE INTO Accounts (username, password, added_at, is_valid, last_validated_at, platform_id) values (?, ?, ?, ?, ?, ?)',
                       (new_account.username, new_account.password, new_account.validated_at, bool(new_account.is_valid), new_account.validated_at, new_account.platform_id))
    
        self._main_conn.commit()
        cursor.close()
    
    def insert_new_auth(self, new_account: Account=Account) -> None:
        """Insere uma nova autenticação no banco de dados."""
        cursor = self._main_conn.cursor()
        account_id = cursor.execute('SELECT id FROM Accounts WHERE username like ?', (f'%{new_account.username.lower()}%',)).fetchone()[0]
        cursor.execute('INSERT OR UPDATE INTO Auths (account_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data) values (?, ?, ?, ?, ?, ?)',
                       (account_id, new_account.auth_token, new_account.auth_token_expires_at, new_account.refresh_token, new_account.refresh_token_expires_at, new_account.other_data))
        self._main_conn.commit()
        cursor.close()
    
    def get_accounts(self) -> Tuple[sqlite3.Row, ...]:
        """Retorna todas as contas do banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT * from Accounts')
        accounts = cursor.fetchall()
        cursor.close()
        return accounts
    
    def get_account(self, account_id: int) -> sqlite3.Row:
        """Retorna uma conta específica do banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT * from Accounts WHERE id = ?', (account_id,))
        account = cursor.fetchone()
        cursor.close()
        return account

    def update_account(self, account_id: int, new_account: Account=Account) -> Account:
        """Atualiza uma conta específica do banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('UPDATE Accounts SET username = ?, password = ?, platform_id = ? WHERE id = ?',
                       (new_account.username, new_account.password, new_account.platform_id, account_id))
        self._main_conn.commit()
        cursor.close()
        return new_account
    
    def delete_account(self, account_id: int) -> None:
        """Deleta uma conta específica do banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('DELETE FROM Accounts WHERE id = ?', (account_id,))
        self._main_conn.commit()
        cursor.close()
    
    def check_account_session(self, account: Account=Account) -> sqlite3.Row:
        """Retorna os dados da conta que existem na DB para manipulação posterior."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT Accounts.*, Auths.* FROM Accounts JOIN Auths ON Accounts.id = Auths.account_id WHERE Accounts.username like ?', 
                       (f'%{account.username.lower()}%',))
        account = cursor.fetchone()
        cursor.close()
        return account

    def get_all_settings(self) -> Tuple[sqlite3.Row, ...]:
        """Retorna todas as configurações do banco de dados."""
        cursor = self._main_conn.cursor()
        cursor.execute('SELECT * from Settings')
        settings = cursor.fetchall()
        cursor.close()
        return settings
