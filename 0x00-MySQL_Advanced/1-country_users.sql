-- This scirpt creates a 'users' table with 'id', 'email', 'name', and 
-- 'country' fields. The 'country' field has a defailt value and a check constraint.
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
