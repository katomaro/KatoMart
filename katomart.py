"""Ponto de inicialização para um futuro server Flask"""

from flask import Flask, render_template, jsonify, g

from modules.databases.manager_main import ManagerMain


app = Flask(__name__,
             template_folder='modules/front/templates',
               static_folder='modules/front/static'
            )
app.config['TEMPLATES_AUTO_RELOAD'] = True


def db_as_a_service(): # we do some clowning here
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = ManagerMain()
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')
@app.route('/api/get_accounts')
def get_accounts():
    database_manager = ManagerMain()
    all_accounts = database_manager.get_accounts()
    return jsonify(all_accounts)
@app.route('/api/get_auths')
def get_auths():
    database_manager = ManagerMain()
    auths = database_manager.get_auths()
    return jsonify(auths)

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/support')
def support():
    return render_template('support.html')


if __name__ == '__main__':
    PORTA = 6102
    print('[INIT] Por favor, ignore todos os textos abaixo/acima, vá até o seu '
          f'navegador e acesse o endereço http://localhost:{PORTA}\n'
          'Estes textos são apenas de debug. Não feche esse terminal enquanto '
          'estiver utilizando o Katomart em sua interface web (porém você pode '
          'fechar o navegador e voltar até o site para gerenciar o Katomart quando quiser')

    app.run(debug=True, port=PORTA)
