-- Configuração de suporte a chaves estrangeiras pq sqlite é abluebleublbuebleube
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT NOT NULL,
    sensitive_data INTEGER DEFAULT 0 CHECK(sensitive_data IN (0, 1)), -- Indica se contém dados sensíveis
    log_data TEXT NOT NULL,
    log_created_at INTEGER NOT NULL -- EPOCH da criação do log
);

CREATE TABLE IF NOT EXISTS MediaDeliverySources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- Nome do player ou tipo de conteúdo (ex.: 'Arquivo Direto', 'Link Drive', 'Youtube', 'Vimeo')
    description TEXT, -- Descrição opcional do tipo de entrega de conteúdo
    download TEXT DEFAULT '0'
);

CREATE TABLE IF NOT EXISTS DRMTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- Nome do tipo de DRM (ex.: 'SOCIAL', 'REAL', 'Widevine')
    description TEXT, -- Descrição opcional do DRM, indicará se vai ser suportado ou não o download e o motivo
    download TEXT DEFAULT '0'
);

CREATE TABLE IF NOT EXISTS Platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    landing_page TEXT UNIQUE NOT NULL,
    content_delivery_type TEXT NOT NULL,
    last_accessed_at INTEGER DEFAULT 0,
    ip_banned INTEGER DEFAULT 0 CHECK(ip_banned IN (0, 1))
);

CREATE TABLE IF NOT EXISTS PlatformDRM (
    platform_id INTEGER NOT NULL,
    drm_type_id INTEGER NOT NULL,
    PRIMARY KEY (platform_id, drm_type_id),
    FOREIGN KEY (platform_id) REFERENCES Platforms(id) ON DELETE CASCADE,
    FOREIGN KEY (drm_type_id) REFERENCES DRMTypes(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT,
    added_at INTEGER NOT NULL, -- Timestamp UNIX da adição da conta
    is_valid INTEGER DEFAULT 0 CHECK(is_valid IN (0, 1)),
    last_validated_at INTEGER DEFAULT 0,
    platform_id INTEGER NOT NULL REFERENCES Platforms(id) ON DELETE CASCADE,
    UNIQUE(username, platform_id)
);

CREATE TABLE IF NOT EXISTS Courses (
    id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    course_url TEXT NOT NULL,
    downloaded_at INTEGER DEFAULT 0,
    last_verified_at INTEGER DEFAULT 0,
    platform_id INTEGER NOT NULL REFERENCES Platforms(id) ON DELETE CASCADE,
    PRIMARY KEY (id, platform_id)
);

CREATE TABLE IF NOT EXISTS Auths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES Accounts(id) ON DELETE CASCADE,
    platform_id INTEGER NOT NULL REFERENCES Platforms(id) ON DELETE CASCADE,
    auth_token TEXT NOT NULL,
    auth_token_expires_at INTEGER NOT NULL, -- EPOCH de expiração do token
    refresh_token TEXT NOT NULL,
    refresh_token_expires_at INTEGER NOT NULL, -- EPOCH de expiração do token de refresh
    other_data TEXT, -- Dados adicionais da sessão em formato JSON em string
    UNIQUE(platform_id, account_id)
);
