DELIMITER //

CREATE TRIGGER copy_to_paid_violation
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    -- Copy the corresponding entry from violation to paid_violation
    INSERT INTO paid_violation (violation_id, viol_type, dt_time, amount, loc, zone_id, vehicle_no)
    SELECT violation_id, viol_type, dt_time, amount, loc, zone_id, vehicle_no
    FROM violation
    WHERE violation_id = NEW.violation_id;

    -- Delete the entry from the violation table
    DELETE FROM violation
    WHERE violation_id = NEW.violation_id;
END;

//

DELIMITER ;
