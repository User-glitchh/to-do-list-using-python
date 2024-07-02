
-- ------------------------------------------------------------------------------------------------

CREATE DATABASE todo_app;

USE todo_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile numeric NOT NULL
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    task VARCHAR(255),
    status VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------------------------------------

-- to activate cursor on database named todo_app
USE todo_app;

-- fetch all the entries of users table in todo_app
SELECT * FROM users;

-- fetch all the entries of tasks table in todo_app
SELECT * FROM tasks;
