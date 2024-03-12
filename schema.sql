-- Creation of the "padel" database
CREATE DATABASE IF NOT EXISTS padel;

-- Creation of the "admin" user
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON padel.* TO 'admin'@'%';

-- Use the "padel" database
USE padel;

-- Creation of the "user" table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(512) NOT NULL COMMENT 'User email',
    password VARCHAR(256) NOT NULL COMMENT 'User password'
    role INT NOT NULL DEFAULT 1 COMMENT 'User role',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'User creation date'
    last_login_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'User last login date'

    UNIQUE(email),
    INDEX (email)
);

-- Creation of the "reservation" table
CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT 'User id',
    match_data DATETIME NOT NULL COMMENT 'Math date'
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Reservation creation date'
    
    UNIQUE(user_id, match_data),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (match_data)
);
