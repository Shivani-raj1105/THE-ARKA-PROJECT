-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    bio TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Plant detection tasks table
CREATE TABLE IF NOT EXISTS plant_tasks (
    task_id TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    input_file_path TEXT,
    result TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
