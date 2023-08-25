-- Show all tables
SHOW TABLES;

-- Show all databases
SHOW DATABASES;

-- Show all users
SELECT User FROM mysql.user;

-- Show all entries in the application user table
SELECT username FROM user;

-- Create a new user new_user with password "very_secret"
CREATE USER IF NOT EXISTS 'new_user'@'localhost' IDENTIFIED BY 'very_secret';

-- Modify user permissions to read a table
GRANT SELECT ON car_manufacturer_v2 TO 'new_user'@'localhost';

-- Revoke the previously granted permission
REVOKE SELECT ON car_manufacturer_v2 FROM 'new_user'@'localhost';

-- Drop the user created
DROP USER 'new_user'@'localhost';

-- Do a SELECT everything statement on the cars table
SELECT * FROM car_model_v1;

-- Do an UPDATE to a car in the cars table
UPDATE car_model_v1 SET name = 'Fabia' WHERE name = 'Octavia' LIMIT 1;
UPDATE car_model_v1 SET name = 'Octavia' WHERE name = 'Fabia' LIMIT 1;

-- Use a SELECT on the cars table using a cursor
DECLARE my_cursor CURSOR FOR SELECT * FROM car_model_v1;
OPEN my_cursor;
FETCH my_cursor INTO variables;
CLOSE my_cursor;

OPEN my_cursor;

-- Loop to fetch and process rows
WHILE TRUE DO
    FETCH my_cursor INTO variable1, variable2;
    IF @@SQLSTATUS <> 0 THEN
        LEAVE;
    END IF;
    -- Process data in variable1 and variable2
END WHILE;

CLOSE my_cursor;

-- Make a compex function
CREATE FUNCTION IF NOT EXISTS fetch_and_return_columns(table_name VARCHAR(50))
RETURNS VARCHAR(100)
BEGIN
    DECLARE variable1 VARCHAR(50);
    DECLARE variable2 VARCHAR(50);
    DECLARE result VARCHAR(100);

    -- TODO: use table_name
    -- SET @query = CONCAT('SELECT id, name FROM ', table_name);
    -- PREPARE my_cursor FROM @query;
    DECLARE my_cursor CURSOR FOR SELECT id, name FROM car_model_v1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @no_more_rows = TRUE;

    OPEN my_cursor;

    SET result = '';
    SET @no_more_rows = FALSE;

    -- Loop to fetch and process rows
    FETCH_LOOP: LOOP
        FETCH my_cursor INTO variable1, variable2;
        IF @no_more_rows THEN
            LEAVE FETCH_LOOP;
        END IF;

        SET result = CONCAT(result, 'Column 1: ', variable1, ', Column 2: ', variable2, '\n');
    END LOOP;

    CLOSE my_cursor;

    RETURN result;
END;


-- Use this function
SELECT fetch_and_return_columns('car_model_v1');

-- Drop the function
DROP FUNCTION IF EXISTS fetch_and_return_columns;

-- Use a trigger

CREATE TRIGGER trigger_name BEFORE/AFTER INSERT/UPDATE/DELETE ON car_model_v1
FOR EACH ROW
BEGIN
    -- Trigger logic here
END;

-- Trigger to avoid duplicate names in the car table
CREATE TRIGGER check_duplicate_name
AFTER INSERT ON car_model_v1
FOR EACH ROW
BEGIN
    DECLARE duplicate_count INT;

    SELECT COUNT(*) INTO duplicate_count
    FROM car_model_v1
    WHERE name = NEW.name;

    IF duplicate_count > 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate name entry found';
    END IF;
END;

-- procedures
CREATE PROCEDURE log_before_insert()
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Logging before insert from the procedure';
END;

CREATE TRIGGER log_before_insert_trigger
BEFORE INSERT ON car_manufacturer_v2
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Logging before insert from the trigger';
    CALL log_before_insert();
END;

DROP TRIGGER IF EXISTS log_before_insert_trigger;
DROP PROCEDURE IF EXISTS log_before_insert;

-- index by time of creation
CREATE INDEX idx_timestamp_created ON car_manufacturer_v2 (timestamp_created);

DROP INDEX idx_timestamp_created ON car_manufacturer_v2;

-- Start a transaction
START TRANSACTION;

-- Commit the transaction
COMMIT;

-- Rollback
ROLLBACK;
