CREATE DATABASE final_project_database;

CREATE TABLE user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
); 

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    author_id INT REFERENCES user(user_id),
    postNum_likes INT,
    timestamp TIMESTAMP,
    caption VARCHAR(200)
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(post_id),
    user_id INT REFERENCES user(user_id)
    text TEXT,
    commentNum_likes INT
);

CREATE TABLE likes (
   like_id SERIAL PRIMARY KEY,
   user_id INT REFERENCES user(user_id),
   post_id INT REFERENCES posts(post_id),
   comment_id  INT REFERENCES comments(comment_id),
   liked_at TIMESTAMP
   );
