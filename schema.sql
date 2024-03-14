-- Creation of the "padel" database
CREATE DATABASE IF NOT EXISTS padel_time;

-- Creation of the "admin" user
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON padel_time.* TO 'admin'@'%';

-- Use the "padel_time" database
USE padel_time;

-- Creation of the "user" table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(512) NOT NULL COMMENT 'User email',
    password VARCHAR(256) NOT NULL COMMENT 'User password',
    role INT NOT NULL DEFAULT 1 COMMENT 'User role',
    last_login_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'User last login date',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'User creation date',

    UNIQUE (email),
    INDEX (email)
);

-- Creation of the "game" table
CREATE TABLE IF NOT EXISTS game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot DATETIME NOT NULL COMMENT 'Game date',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Game creation date',
    created_by INT NOT NULL COMMENT 'User id',
    
    FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE CASCADE,
    
    UNIQUE (slot),
    INDEX (slot)
);

-- Creation of the "game_user" table
CREATE TABLE IF NOT EXISTS game_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL COMMENT 'Game id',
    user_id INT NOT NULL COMMENT 'User id',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Game user creation date',
    
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    
    UNIQUE(game_id, user_id),
    INDEX (game_id),
    INDEX (user_id)
);
