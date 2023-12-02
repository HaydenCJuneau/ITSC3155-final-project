CREATE DATABASE final_project_database;

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    image BYTEA NOT NULL,
    title VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    description TEXT,
    status VARCHAR(255) NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY(author_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    post_id INT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(post_id),
    FOREIGN KEY(author_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS likes (
   like_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
   FOREIGN KEY(user_id) REFERENCES users(user_id),
   FOREIGN KEY(post_id) REFERENCES posts(post_id)
);