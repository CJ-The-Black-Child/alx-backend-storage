-- This script creates a stored procedire that adds a new correction.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_id INT DEFAULT 0;

    INSERT INTO projects(name)
    ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id), name = VALUES(name);

    SET project_id = LAST_INSERT_ID();

    INSERT INTO corrections(user_id, project_id, score)
    VALUES (user_id, project_id, score);
END $$
DELIMITER ;
