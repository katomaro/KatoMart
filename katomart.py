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
        
@app.route('/agreement')
def agreement():
    return render_template('agreement.html')

@app.route('/api/agreement', methods=['POST'])
def update_agreement():
    db_manager = get_db()
    if request.form.get('agreement'):
        db_manager.update_setting('user_consent', int(bool((request.form.get('agreement')))))
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    return render_template('home.html')

@app.route('/settings')
def settings():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    selected_settings = db_manager.get_all_settings()
    media_types = db_manager.get_all_media_delivery_sources()
    media_types = [(x[0], x[1], not bool(x[2])) for x in media_types]
    drm_types = db_manager.get_all_drm_types()
    drm_types = [(x[0], x[1], not bool(x[2])) for x in drm_types]
    selected_settings.update({'media_types': media_types, 'drm_types': drm_types})
    selected_settings['use_custom_ffmpeg'] = bool(selected_settings['use_custom_ffmpeg'])
    return render_template('settings.html', settings=selected_settings)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    db_manager = get_db()
    if request.form.get('download_path'):
        db_manager.update_setting('download_path', request.form.get('download_path'))
    if request.form.get('download_from_players'):
        db_manager.update_setting('download_from_players', request.form.get('download_from_players'))
    if request.form.get('download_drm_content'):
        db_manager.update_setting('download_drm_content', request.form.get('download_drm_content'))
    if request.form.get('download_drm_types'):
        db_manager.update_setting('download_drm_types', request.form.get('download_drm_types'))
    if request.form.get('default_user_agent'):
        db_manager.update_setting('default_user_agent', request.form.get('default_user_agent'))
    if request.form.get('use_custom_ffmpeg'):
        db_manager.update_setting('use_custom_ffmpeg', request.form.get('use_custom_ffmpeg'))
    if request.form.get('custom_ffmpeg_path'):
        db_manager.update_setting('custom_ffmpeg_path', request.form.get('custom_ffmpeg_path'))
    return redirect(url_for('settings'))

@app.route('/accounts')
def accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    return render_template('accounts.html')

@app.route('/api/get_accounts')
def get_accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify([])
    all_accounts = []
    return jsonify(all_accounts)

@app.route('/api/get_auths')
def get_auths():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify([])
    auths = []
    return jsonify(auths)

@app.route('/courses')
def courses():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    return render_template('courses.html')

@app.route('/log')
def log():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    return render_template('log.html')

@app.route('/support')
def support():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
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
