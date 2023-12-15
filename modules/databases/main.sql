-- NUNCA JAMAIS ALTERAR AS IDS DAS PLATAFORMAS INSERIDAS AQUI!
CREATE TABLE IF NOT EXISTS Platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID incremental para cada plataforma
    name TEXT UNIQUE NOT NULL, -- Nome de Marca da Plataforma
    description TEXT, -- Descricao breve do conteúdo encontrado na plataforma e sua disponibilizacao
    landing_page TEXT UNIQUE NOT NULL, -- URL da pagina inicial da plataforma
    content_delivery_type TEXT NOT NULL, -- Tipo de entrega de conteúdo da plataforma API/HTML
    has_drm INTEGER DEFAULT 0,
    drm_type TEXT,
    last_accessed_at INTEGER DEFAULT 0, -- Qyabdi foi a ultima vez que a plataforma foi acessada
    ip_banned INTEGER DEFAULT 0 -- Se o IP do cliente está banido da plataforma
);

-- NUNCA JAMAIS DROPAR ESSA TABELA POR QUEBRAR OS DADOS DO USUÁRIO!
CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID Incremental de cada conta adicionada ao sistema
    username TEXT NOT NULL, -- Username ou Email da conta que possui o produto
    password TEXT, -- Senha da conta que possui o produto
    is_valid INTEGER DEFAULT 0, -- Se a conta está autenticando ou não
    validated_at INTEGER DEFAULT 0, -- Quando a conta foi adicionada como válida
    has_authenticated INTEGER DEFAULT 0, -- Se a conta possui sessão ativa na plataforma
    authenticated_at INTEGER DEFAULT 0, -- Quando a sessão foi criada
    authentication_token TEXT, -- O token de autorização da sessão
    authentication_token_expires_at INTEGER DEFAULT 0, -- A data de expiração do Token
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
