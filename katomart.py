from pathlib import Path
import time
from flask import Flask, request, redirect, render_template, url_for, jsonify, g
from modules.databases.manager_main import DatabaseManager

from modules.accounts.hotmart import Hotmart

platform_classes = {
    1: Hotmart,
}


app = Flask(__name__, 
            template_folder='modules/front/templates',
            static_folder='modules/front/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

execution_path = Path(__file__).parent
db_folder_path = execution_path / 'modules' / 'databases'
database_path = execution_path / 'main.sqlite3'
def get_db():
    """
    Obtém uma instância do gerenciador de banco de dados, seguindo o padrão application factory.
    """
    if 'db' not in g:
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

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    g.pop('selected_platform_instance', None)

# Rotas do aplicativo
        
@app.route('/agreement')
def agreement():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    return render_template('agreement.html', consent=consent)

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

    drm_types = db_manager.get_all_drm_types()

    selected_settings.update({'media_types': media_types, 'drm_types': drm_types})
    selected_settings['use_custom_ffmpeg'] = bool(selected_settings['use_custom_ffmpeg'])

    drm_types = [(x[0], x[1], bool(x[2])) for x in drm_types]

    selected_settings.update({"media_types": media_types, "drm_types": drm_types})

    return render_template("settings.html", settings=selected_settings)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    db_manager = get_db()

    field_settings = [
        "download_path",
        "default_user_agent",
    ]

    # acredito que isso daqui venha depois...
    field_boolean_settings = [
        # "download_from_players",
        # "download_drm_content",
        # "download_drm_types"
    ]

    if request.form.get("use_custom_ffmpeg") == "on":
        db_manager.update_setting("use_custom_ffmpeg", 1)
        db_manager.update_setting(
            "custom_ffmpeg_input",
            request.form.get("custom_ffmpeg_input") or "SYSTEM",
        )
    else:
        db_manager.update_setting("use_custom_ffmpeg", 0)

    for field in field_settings:
        value = request.form.get(field, None)
        if value == "on":
            value = True
        if value is not None:
            db_manager.update_setting(field, value)

    for field in field_boolean_settings:
        value = request.form.get(field, None) == "on"
        db_manager.update_setting(field, value)

    media_types = db_manager.get_all_media_delivery_sources()
    for name, _, download in media_types:
        value = request.form.get(name)
        value = 1 if value == "on" else 0
        if value != download:
            db_manager.update_media_delivery_source_download(name, value)
            
    drm_types = db_manager.get_all_drm_types()
    for name, _, download in drm_types:
        value = request.form.get(name)
        value = 1 if value == "on" else 0
        if value != download:
            db_manager.update_drm_type_download(name, value)

    return redirect(url_for("settings"))

@app.route('/accounts')
def accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return redirect(url_for('agreement'))
    return render_template('accounts.html')

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify([])
    platforms = db_manager.fetch_platforms()
    return jsonify(platforms)

@app.route('/api/get_accounts')
def get_accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify([])

    platform_id = request.args.get('platform_id', default=None, type=int)
    if platform_id is None:
        return jsonify([])  # Ou retorne um erro, dependendo da sua lógica de aplicação

    # Substitua a chamada abaixo pela sua lógica de busca de contas associadas à plataforma
    all_accounts = db_manager.get_accounts_by_platform(platform_id)
    return jsonify(all_accounts)

@app.route('/api/accounts', methods=['POST'])
def add_or_update_account():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify({'success': False})
    
    # Usar request.json para acessar os dados enviados em formato JSON
    data = request.json
    platform_id = data['platform_id']
    username = data['username']
    password = data['password']
    added_at = int(time.time())
    is_valid = data.get('is_valid', False)
    last_validated_At = int(time.time()) if is_valid else None

    db_manager.add_or_update_account(platform_id, username, password, added_at, last_validated_At, is_valid)
    return jsonify({'success': True})

@app.route('/api/get_session_token', methods=['GET'])
def get_session_token():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify({'success': False})
    platform_id = request.args.get('platform_id')
    username = request.args.get('username')
    token_info = db_manager.get_session_token_by_email(platform_id, username)
    if token_info:
        return jsonify({'success': True, 'token': token_info['auth_token'], 'expires_at': token_info['auth_token_expires_at']})
    else:
        return jsonify({'success': False})

@app.route('/api/update_token', methods=['POST'])
def update_token():
    db_manager = get_db()
    consent = int(db_manager.get_setting('user_consent'))
    if not consent:
        return jsonify({'success': False})
    account_id = request.form['account_id']
    platform_id = request.form['platform_id']
    auth_token = request.form['auth_token']
    auth_token_expires_at = request.form['auth_token_expires_at']
    refresh_token = request.form['refresh_token']
    refresh_token_expires_at = request.form['refresh_token_expires_at']
    other_data = request.form.get('other_data', '')  # Dados adicionais são relativos

    db_manager.update_auth_token(account_id, platform_id, auth_token, auth_token_expires_at, refresh_token, refresh_token_expires_at, other_data)
    
    return jsonify({'success': True})

@app.route('/api/select_account', methods=['POST'])
def select_account():
    account_id = int(request.json.get('account_id'))
    platform_id = int(request.json.get('platform_id'))

    if not account_id or not platform_id:
        return jsonify({"error": "Account ID and Platform ID are required."}), 400

    platform_class = platform_classes.get(platform_id)
    if not platform_class:
        return jsonify({"error": "Invalid Platform ID."}), 400

    g.selected_platform_instance = platform_class(account_id, DatabaseManager(db_folder_path=db_folder_path, db_path=database_path))

    return jsonify({"message": f"Platform instance for account {account_id} selected."})


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
