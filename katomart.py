"""Ponto de inicialização para um futuro server Flask"""

from flask import Flask, render_template

from modules.databases.manager_main import ManagerMain
from modules.accounts.hotmart import Hotmart


app = Flask(__name__, template_folder='modules/templates')

@app.route('/')
def katomart_root():
    return render_template('index.html')


if __name__ == '__main__':
    # manager = ManagerMain()
    # print(manager.get_supported_platforms())
    # account = Hotmart('teste', 'teste', database_manager=manager)
    # a = manager.insert_new_account(account)
    # print(a)

    app.run(debug=True, port=6102)
