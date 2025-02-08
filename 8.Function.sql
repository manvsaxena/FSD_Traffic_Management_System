DELIMITER //

CREATE FUNCTION calculate_total_amount_paid(zone_id_param INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE total_amount INT;

    SELECT SUM(amount)
    INTO total_amount
    FROM paid_violation
    WHERE zone_id = zone_id_param;

    IF total_amount IS NULL THEN
        SET total_amount = 0;
    END IF;

    RETURN total_amount;
END //

DELIMITER ;

DELIMITER //

CREATE FUNCTION calculate_total_amount_pending(zone_id_param INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE total_amount INT;

    SELECT SUM(amount)
    INTO total_amount
    FROM violation
    WHERE zone_id = zone_id_param;

    IF total_amount IS NULL THEN
        SET total_amount = 0;
    END IF;

    RETURN total_amount;
END //

DELIMITER ;