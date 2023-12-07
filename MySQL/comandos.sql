-- Active: 1699533413856@@127.0.0.1@3306@comidaria
#CREATE DATABASE comidaria;
USE comidaria;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

SELECT * FROM receitas

SELECT * FROM users