--
-- File generated with SQLiteStudio v3.4.3 on śr. kwi 5 18:07:54 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: movies
CREATE TABLE IF NOT EXISTS movies(
    id TEXT NOT NULL PRIMARY KEY,
    filename TEXT NOT NULL,
    title TEXT NOT NULL,
    series TEXT NULL,
    episode INTEGER NULL,
    FOREIGN KEY(series) REFERENCES series(id)
);

-- Table: series
CREATE TABLE IF NOT EXISTS series(
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL
);

-- Table: users
CREATE TABLE IF NOT EXISTS users(
    id TEXT NOT NULL PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    added_on TEXT NOT NULL,
    permission_level INTEGER NOT NULL
);

-- Table: watch_list
CREATE TABLE IF NOT EXISTS watch_list(
    movie_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    added_on TEXT NOT NULL,
    watched BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY(movie_id, user_id),
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Table: watch_time
CREATE TABLE IF NOT EXISTS watch_time(
    movie_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    watched_on TEXT NOT NULL,
    watch_time INT NOT NULL,
    PRIMARY KEY(movie_id, user_id),
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
