#CREATE DATABASE comidaria;
USE comidaria;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE Table receita(id_user INT PRIMARY KEY AUTO_INCREMENT, nome_da_receita VARCHAR(255) NOT NULL,
Modo_de_preparo VARCHAR (500) NOT NULL);

Alter Table users ADD CONSTRAINT fk_idcliente Foreign Key (id) REFERENCES (receita) (id_users)
