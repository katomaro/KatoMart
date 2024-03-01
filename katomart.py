from pathlib import Path
from flask import Flask, request, redirect, render_template, url_for, jsonify, g
from modules.databases.manager_main import DatabaseManager

# Configuração inicial do aplicativo Flask
app = Flask(__name__, 
            template_folder='modules/front/templates',
            static_folder='modules/front/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
    """
    Obtém uma instância do gerenciador de banco de dados, seguindo o padrão application factory.
    """
    if 'db' not in g:
        execution_path = Path(__file__).parent
        db_folder_path = execution_path / 'modules' / 'databases'
        database_path = execution_path / 'main.sqlite3'
        g.db = DatabaseManager(db_folder_path=db_folder_path, db_path=database_path)
    return g.db

@app.teardown_appcontext
def close_db(error):
    """
    Fecha a conexão com o banco de dados ao finalizar o contexto da aplicação.
    """
    db = g.pop('db', None)
    if db is not None:
        del db

# Rotas do aplicativo
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/settings')
def settings():
    db_manager = get_db()
    settings = db_manager.get_all_settings()
    media_types = db_manager.get_all_media_delivery_sources()
    drm_types = db_manager.get_all_drm_types()
    settings.update({'media_types': media_types, 'drm_types': drm_types})
    settings['use_custom_ffmpeg'] = bool(settings['use_custom_ffmpeg'])
    return render_template('settings.html', settings=settings)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    db_manager = get_db()
    if request.form.get('download_path'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('some_setting'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    return redirect(url_for('settings'))

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

# @app.route('/api/get_accounts')
# def get_accounts():
#     database_manager = get_db()
#     all_accounts = database_manager.get_accounts()
#     return jsonify(all_accounts)

# @app.route('/api/get_auths')
# def get_auths():
#     database_manager = get_db()
#     auths = database_manager.get_auths()
#     return jsonify(auths)

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
