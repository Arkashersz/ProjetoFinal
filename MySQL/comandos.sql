-- Active: 1699533413856@@127.0.0.1@3306@comidaria
#CREATE DATABASE comidaria;
USE comidaria;
CREATE TABLE users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE receitas (
    user_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    ingredientes TEXT NOT NULL,
    preparo TEXT NOT NULL,
    post_id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

SELECT * FROM receitas

SELECT * FROM users