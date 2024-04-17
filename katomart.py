import time
from pathlib import Path

from flask import (
    Blueprint,
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from modules.accounts.hotmart import Hotmart
from modules.databases.manager_main import DatabaseManager
from modules.downloaders.main_downloader import Downloader


platform_classes = {
    1: Hotmart,
}

Downloader_instance = None

app = Flask(
    __name__, template_folder="modules/front/templates", 
    static_folder="modules/front/static"
)

app.config["TEMPLATES_AUTO_RELOAD"] = True

execution_path = Path(__file__).parent
db_folder_path = execution_path / "modules" / "databases"
database_path = execution_path / "main.sqlite3"


def get_db():
    """
    Obtém uma instância do gerenciador de banco de dados, seguindo o padrão application factory.
    """
    if "db" not in g:
        g.db = DatabaseManager(db_folder_path=db_folder_path, db_path=database_path)
    return g.db


@app.teardown_appcontext
def close_db(error):
    """
    Fecha a conexão com o banco de dados ao finalizar o contexto da aplicação.
    """
    db = g.pop("db", None)
    if db is not None:
        del db


selected_platform_instance = None

# Rotas do aplicativo
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/agreement")
def agreement():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent")) == 1
    return jsonify({"consent": consent})


@api_bp.route("/agreement", methods=["POST"])
def update_agreement():
    db_manager = get_db()
    if request.form.get("agreement"):
        db_manager.update_setting("user_consent", int(request.form["agreement"] == "on"))
    return redirect(url_for("index"))


@app.route("/")
@app.route("/<path:_>")
def index(_=None):
    return render_template("index.html")


@api_bp.post("/save_user_state")
def save_user_state():
    data = request.json
    if not data:
        return "error", 400
    db_manager = get_db()
    last_executed_at = int(time.time())
    db_manager.update_setting("last_executed_at", last_executed_at)
    db_manager.update_setting("user_os", data.get("user_os", ""))

    return "ok"


@api_bp.get("/settings")
def settings():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return redirect(url_for("agreement"))
    selected_settings = db_manager.get_all_settings()

    media_delivery_types = db_manager.get_all_media_delivery_sources()

    drm_types = db_manager.get_all_drm_types()

    media_types = db_manager.get_all_media_types()

    selected_settings["use_custom_ffmpeg"] = bool(selected_settings["use_custom_ffmpeg"])
    selected_settings["download_widevine"] = bool(selected_settings["download_widevine"])

    selected_settings.update(
        {
            "media_delivery_types": media_delivery_types,
            "media_types": media_types,
            "drm_types": drm_types,
        }
    )

    return jsonify(
        {"settings": selected_settings, "disable_download_btn": bool(selected_platform_instance)}
    )


@api_bp.post("/settings")
def update_settings():
    db_manager = get_db()

    form = request.json

    if not form:
        return jsonify({"success": False, "message": "Dados inválidos... Chame suporte."}), 400

    db_manager.update_setting("use_custom_ffmpeg", int(form.get("use_custom_ffmpeg")))
    db_manager.update_setting("custom_ffmpeg_path", form.get("custom_ffmpeg_path", None) or "SYSTEM")

    db_manager.update_setting("download_widevine", int(form.get("download_widevine", False)))
    db_manager.update_setting("widevine_cdm_path", form.get("widevine_cdm_path", None) or "SYSTEM")
    db_manager.update_setting("bento4_toolbox_path", form.get("bento4_toolbox_path", None) or "SYSTEM")
    
    db_manager.update_setting("get_product_extra_info", int(form.get("get_product_extra_info", False)))

    for field in ["download_path", "default_user_agent", "download_threads"]:
        value = form.get(field, None)
        if value is not None:
            db_manager.update_setting(field, value)

    for media_type in form.get("media_types", []):
        value = int(media_type.get("download", False))
        name = media_type.get("name", None)
        if name is not None:
            db_manager.update_media_type_download(name, value)

    for drm_type in form.get("drm_types", []):
        value = int(drm_type.get("download", False))
        name = drm_type.get("name", None)
        if name is not None:
            db_manager.update_drm_type_download(name, value)

    for media_delivery_type in form.get("media_delivery_types", []):
        value = int(media_delivery_type.get("download", False))
        name = media_delivery_type.get("name", None)
        if name is not None:
            db_manager.update_media_delivery_source_download(name, value)

    return jsonify({"success": True, "message": "Configurações Atualizadas!"})


@api_bp.route("/accounts")
def accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return redirect(url_for("agreement"))
    return render_template("accounts.html", disable_download_btn=bool(selected_platform_instance))


@api_bp.route("/platforms", methods=["GET"])
def get_platforms():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify([])
    platforms = db_manager.fetch_platforms()
    return jsonify(platforms)


@api_bp.route("/get_accounts")
def get_accounts():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify([])

    platform_id = request.args.get("platform_id", default=None, type=int)
    if platform_id is None:
        return jsonify([])  # Ou retorne um erro, dependendo da sua lógica de aplicação

    # Substitua a chamada abaixo pela sua lógica de busca de contas associadas à plataforma
    all_accounts = db_manager.get_accounts_by_platform(platform_id)
    return jsonify(all_accounts)


@api_bp.route("/accounts", methods=["POST"])
def add_or_update_account():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify({"success": False})

    # Usar request.json para acessar os dados enviados em formato JSON
    data = request.json
    if not data:
        return jsonify({"success": False})
    platform_id = data["platform_id"]
    username = data["username"]
    password = data["password"]
    added_at = int(time.time())
    is_valid = data.get("is_valid", False)
    last_validated_At = int(time.time()) if is_valid else None

    db_manager.add_or_update_account(
        platform_id, username, password, added_at, last_validated_At, is_valid
    )
    return jsonify({"success": True})


@api_bp.route("/get_session_token", methods=["GET"])
def get_session_token():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify({"success": False})
    platform_id = request.args.get("platform_id")
    username = request.args.get("username")
    token_info = db_manager.get_session_token_by_email(platform_id, username)
    if token_info:
        return jsonify(
            {
                "success": True,
                "token": token_info["auth_token"],
                "expires_at": token_info["auth_token_expires_at"],
            }
        )
    else:
        return jsonify({"success": False})


@api_bp.route("/update_token", methods=["POST"])
def update_token():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify({"success": False})
    account_id = request.form["account_id"]
    platform_id = request.form["platform_id"]
    auth_token = request.form["auth_token"]
    auth_token_expires_at = request.form["auth_token_expires_at"]
    refresh_token = request.form["refresh_token"]
    refresh_token_expires_at = request.form["refresh_token_expires_at"]
    other_data = request.form.get("other_data", "")  # Dados adicionais são relativos

    db_manager.update_auth_token(
        account_id,
        platform_id,
        auth_token,
        auth_token_expires_at,
        refresh_token,
        refresh_token_expires_at,
        other_data,
    )

    return jsonify({"success": True})


@api_bp.route("/select_account", methods=["POST"])
def select_account():
    global selected_platform_instance
    if not request.json:
        return jsonify({"error": "No JSON data provided."}), 400
    account_id = int(request.json.get("account_id"))
    platform_id = int(request.json.get("platform_id"))

    if not account_id or not platform_id:
        return jsonify({"error": "Account ID and Platform ID are required."}), 400

    platform_class = platform_classes.get(platform_id)
    if not platform_class:
        return jsonify({"error": "Invalid Platform ID."}), 400

    selected_platform_instance = platform_class(
        account_id, DatabaseManager(db_folder_path=db_folder_path, db_path=database_path)
    )

    return jsonify({"message": f"Platform instance for account {account_id} selected."})


@api_bp.route("/delete_account", methods=["POST"])
def delete_account():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return jsonify({"success": False})
    data = request.get_json()  # Obter os dados enviados como JSON
    account_id = data.get("account_id")

    if account_id:
        db_manager.delete_account(account_id)

    return jsonify({"success": True})


@api_bp.route("/courses")
def courses():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return redirect(url_for("index"))
    extra_data = int(db_manager.get_setting("get_product_extra_info"))
    download_path = db_manager.get_setting("download_path")

    global selected_platform_instance
    if selected_platform_instance is None:
        return jsonify({"error": "Nenhuma Conta Selecionada."}), 400

    dl_courses = selected_platform_instance.get_account_products(get_extra_info=extra_data)
    for course in dl_courses:
        course['save_path'] = Path(__file__).parent / download_path
        course['save_path'] = str(course['save_path'].resolve())
    
    return jsonify(courses=dl_courses)
    


@api_bp.route("/load_course_data", methods=["POST"])
def load_course_data():
    db_manager = get_db()
    consent = int(db_manager.get_setting("user_consent"))
    if not consent:
        return redirect(url_for("index"))

    data = request.get_json()
    # TODO renomear isso para id no teu post
    course_id = data.get("club")

    global selected_platform_instance
    if selected_platform_instance is None:
        return redirect(url_for("index"))

    return jsonify(selected_platform_instance.get_product_information(course_id))


@api_bp.route("/start_download", methods=["POST"])
def start_download():
    global selected_platform_instance
    global Downloader_instance

    if selected_platform_instance is None:
        return jsonify({'message':"Nenhuma conta Inicializada. Selecione uma conta para iniciar o download. (bug?)"})
    
    if Downloader_instance is not None:
        return jsonify({"message": "Já existe um download em andamento. Acompanhe pela página de logs."})

    data = request.get_json()
    if data.get("courses") is None:
        return jsonify({"message": "Nenhum curso foi selecionado."})

    selected_courses = data["courses"]
    for course in selected_courses:
        if course.get("selected", False):
            selected_platform_instance.download_content(course)
    
    if selected_platform_instance.downloadable_products is not None:
        Downloader_instance = Downloader(selected_platform_instance)
        return jsonify({"message": "Download iniciando, acompanhe pela página Logs."})
    
    return jsonify({"message": "Como você veio parar aqui? Não há cursos selecionados para download!"})

# Raiva ódio e rancor
@api_bp.route('/logs', methods=['GET'])
def api_logs():
    db_manager = get_db()
    int(time.time())
    logs = db_manager.execute_query("SELECT * FROM logs WHERE log_created_at <= ? ORDER BY id DESC LIMIT 1000;", (int(time.time()),)) # (start_date, end_date)

    return jsonify(logs)

@api_bp.route('/courses_progress', methods=['GET'])
def api_courses_progress():
    global Downloader_instance
    return jsonify({'message': 'Este método precisa ser implementado'})


# Ponto de entrada principal para execução do servidor
if __name__ == "__main__":
    PORT = 6102
    print(
        "[INIT] Por favor, ignore todos os textos abaixo/acima, vá até o seu "
        f"navegador e acesse o endereço http://localhost:{PORT}\n"
        "Estes textos são apenas de debug. Não feche esse terminal enquanto "
        "estiver utilizando o Katomart em sua interface web (porém você pode "
        "fechar o navegador e voltar até o site para gerenciar o Katomart quando quiser"
    )
    app.register_blueprint(api_bp)
    app.run(port=PORT)
