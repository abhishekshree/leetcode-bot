CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT,
    url TEXT,
    published BOOLEAN,
    timestamp TEXT
);
