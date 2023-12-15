CREATE TABLE IF NOT EXISTS Platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    landing_page TEXT NOT NULL,
    content_delivery_type TEXT NOT NULL,
    last_accessed_at INTEGER DEFAULT 0,
    ip_banned INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT,
    is_valid INTEGER DEFAULT 0,
    validated_at INTEGER DEFAULT 0,
    has_authenticated INTEGER DEFAULT 0,
    authenticated_at INTEGER DEFAULT 0,
    authentication_token TEXT,
    authentication_token_expires_at INTEGER DEFAULT 0,
    platform_id INTEGER REFERENCES Platforms(id) ON DELETE CASCADE,
    UNIQUE(username, platform_id)
);


CREATE TABLE IF NOT EXISTS Courses (
    id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    course_url TEXT NOT NULL,
    downloaded_at INTEGER DEFAULT 0,
    last_verified_at INTEGER DEFAULT 0,
    platform_id INTEGER REFERENCES Platforms(id) ON DELETE CASCADE,
    UNIQUE(id, platform_id)
);
