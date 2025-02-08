DELIMITER //

CREATE PROCEDURE ReduceAmountInZone(IN zoneIDParam INT, IN percentageParam INT)
BEGIN
    DECLARE reductionFactor DECIMAL(5,2);
    
    -- Convert percentage to a decimal factor
    SET reductionFactor = percentageParam / 100.0;

    -- Update the amount in the paid_violation table for the specified zone
    UPDATE violation
    SET amount = amount - (amount * reductionFactor)
    WHERE zone_id = zoneIDParam;
END //

DELIMITER ;
