CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE topics (
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_slug TEXT REFERENCES topics(slug),
    description TEXT
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    topic_slug TEXT REFERENCES topics(slug),
    text TEXT NOT NULL,
    options TEXT[] NOT NULL,
    answer_index INTEGER NOT NULL,
    difficulty INTEGER DEFAULT 1500,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    correct BOOLEAN,
    time_spent_seconds NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE study_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    goals TEXT[],
    weeks INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE adherence_logs (
    id SERIAL PRIMARY KEY,
    study_plan_id INTEGER REFERENCES study_plans(id),
    week INTEGER,
    completed_tasks INTEGER,
    reflections TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
