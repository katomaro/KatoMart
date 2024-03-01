from flask import Flask, render_template, jsonify, g
from modules.databases.manager_main import ManagerMain

# Configuração inicial do aplicativo Flask
app = Flask(__name__, 
            template_folder='modules/front/templates', 
            static_folder='modules/front/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
    """
    Função para obter uma instância do banco de dados, seguindo o padrão application factory.
    """
    if 'db' not in g:
        g.db = ManagerMain()
    return g.db

@app.teardown_appcontext
def close_db(error):
    """
    Fecha a conexão com o banco de dados ao finalizar o contexto da aplicação.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Rotas do aplicativo
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
    database_manager = get_db()
    all_accounts = database_manager.get_accounts()
    return jsonify(all_accounts)

@app.route('/api/get_auths')
def get_auths():
    database_manager = get_db()
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

# Ponto de entrada principal para execução do servidor
if __name__ == '__main__':
    PORT = 6102
    print('[INIT] Por favor, ignore todos os textos abaixo/acima, vá até o seu '
          f'navegador e acesse o endereço http://localhost:{PORT}\n'
          'Estes textos são apenas de debug. Não feche esse terminal enquanto '
          'estiver utilizando o Katomart em sua interface web (porém você pode '
          'fechar o navegador e voltar até o site para gerenciar o Katomart quando quiser')
    app.run(debug=True, port=PORT)
