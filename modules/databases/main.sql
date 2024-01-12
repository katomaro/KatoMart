CREATE TABLE IF NOT EXISTS GlobalSettings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    database_instanced_at INTEGER DEFAULT 0, -- Quando o banco de dados foi instanciado
    last_executed_at INTEGER DEFAULT 0, -- Quando foi a última vez que o software foi executado
    user_consent INTEGER DEFAULT 0, -- Se o usuário concordou com os termos de uso do software e está ciente dos riscos
    download_path TEXT NOT NULL, -- Caminho para salvar os arquivos baixados
    user_os TEXT NOT NULL, -- Sistema operacional do usuário
    default_user_agent TEXT NOT NULL -- User-Agent padrão para o software
    use_custom_ffmpeg INTEGER DEFAULT 0, -- Se o usuário deseja usar um ffmpeg customizado ao invés do ffmpeg do sistema
);

CREATE TABLE IF NOT EXISTS CustomSettings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL, -- Chave do valor
    value TEXT NOT NULL -- Valor da chave
);

CREATE TABLE IF NOT EXISTS Logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT NOT NULL, -- Tipo de log
    sensitive_data INTEGER DEFAULT 0, -- Se esse log possui dados sensíveis
    log_data TEXT NOT NULL, -- Dados do log
    log_created_at INTEGER DEFAULT 0 -- Quando o log foi criado
);

-- NUNCA JAMAIS ALTERAR AS IDS DAS PLATAFORMAS INSERIDAS AQUI!
CREATE TABLE IF NOT EXISTS Platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID incremental para cada plataforma
    name TEXT UNIQUE NOT NULL, -- Nome de Marca da Plataforma
    description TEXT, -- Descricao breve do conteúdo encontrado na plataforma e sua disponibilizacao
    landing_page TEXT UNIQUE NOT NULL, -- URL da pagina inicial da plataforma
    content_delivery_type TEXT NOT NULL, -- Tipo de entrega de conteúdo da plataforma API/HTML
    has_drm INTEGER DEFAULT 0, -- Se a plataforma possui algum tipo de DRM
    drm_type TEXT, -- Social (DRM FALSO), REAL (Widevine, PlayReady, FairPlay, etc)
    -- No caso de DRM FALSO, se a plataforma renderiza os dados do lado do cliente, ao baixar o arquivo é limpo, não teve
    -- nenhum procedimento para remoção. No caso de DRM REAL, será dado apenas um guia para o usuário seguir para conseguir
    -- realizar o download. Note que em momento algum o sistema irá remover quaisquer dados ocultos dos arquivos.
    last_accessed_at INTEGER DEFAULT 0, -- Qyabdi foi a ultima vez que a plataforma foi acessada
    ip_banned INTEGER DEFAULT 0 -- Se o IP do cliente está banido da plataforma
);

-- NUNCA JAMAIS DROPAR ESSA TABELA POR QUEBRAR OS DADOS DO USUÁRIO!
CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID Incremental de cada conta adicionada ao sistema
    username TEXT NOT NULL, -- Username ou Email da conta que possui o produto
    password TEXT, -- Senha da conta que possui o produto
    added_at INTEGER DEFAULT 0, -- Quando a conta foi criada
    is_valid INTEGER DEFAULT 0, -- Se a conta está autenticando ou não
    last_validated_at INTEGER DEFAULT 0, -- Quando a conta foi validada por último
    platform_id INTEGER REFERENCES Platforms(id) ON DELETE CASCADE, -- A id da plataforma que a conta pertence
    UNIQUE(username, platform_id) -- Cada conta é única para cada plataforma.
);

-- Essa tabela pode ser alterada, porém, não deve ser dropada.
CREATE TABLE IF NOT EXISTS Courses (
    id TEXT NOT NULL, -- A ID do curso na plataforma
    name TEXT NOT NULL, -- Nome do curso
    description TEXT, -- Descrição do curso, se aplicável
    course_url TEXT NOT NULL, -- A URL da landing page do curso
    downloaded_at INTEGER DEFAULT 0, -- Se o download foi concluído, quando?
    last_verified_at INTEGER DEFAULT 0, -- Data da última validação de conteúdo do curso
    platform_id INTEGER REFERENCES Platforms(id) ON DELETE CASCADE, -- Plataforma a qual o curso pertence
    UNIQUE(id, platform_id) -- Cada curso é único para cada plataforma.
);

-- Dropar essa tabela força o usuário a autenticar novamente em todas as contas, lol.
CREATE TABLE IF NOT EXISTS Auths (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID incremental de cada sessão
    account_id INTEGER REFERENCES Accounts(id) ON DELETE CASCADE, -- ID da conta da sessão
    platform_id INTEGER REFERENCES Platforms(id) ON DELETE CASCADE, -- ID da plataforma da sessão
    auth_token TEXT NOT NULL, -- Token da sessão
    auth_token_expires_at INTEGER DEFAULT 0, -- Data de expiração do token // int(time.time())
    refresh_token TEXT NOT NULL, -- Token de atualização da sessão
    refresh_token_expires_at INTEGER DEFAULT 0, -- Data de expiração do token de atualização // int(time.time())
    other_data TEXT, -- Outros dados da sessão, conforme necessário, json convertido para string // json.dumps({})

    UNIQUE(platform_id, account_id) -- Cada site pode ter apenas uma sessão de cada conta
);