-- This script creates a stored procedire that computes and stores the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT IF(COUNT(*) = 0, 0, SUM(score) / COUNT(*))
        FROM corrections
        WHERE user_id = users.id
    )
    WHERE id = user_id;
END $$
DELIMITER ;
