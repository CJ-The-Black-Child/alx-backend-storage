-- Creates a stored procedure 'ComputeAverageWeightedScoreForUser' that 
-- computes and stores the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    SELECT SUM(score * weight) INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE user_id = user_id;

    SELECT SUM(weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE user_id = user_id;

    UPDATE users SET average_score = total_weighted_score / total_weight WHERE id = user_id;
END $$
DELIMITER ;
