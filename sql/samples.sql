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

-- Define a stored procedure
DELIMITER //
CREATE PROCEDURE procedure_name()
BEGIN
    -- Procedure logic here
END;
//

-- Make a compex function
DELIMITER //
CREATE FUNCTION fetch_and_return_columns()
RETURNS VARCHAR(100)
BEGIN
    DECLARE variable1 VARCHAR(50);
    DECLARE variable2 VARCHAR(50);
    DECLARE result VARCHAR(100);

    DECLARE my_cursor CURSOR FOR SELECT column1, column2 FROM my_table;
    OPEN my_cursor;

    SET result = '';

    -- Loop to fetch and process rows
    FETCH_LOOP: WHILE TRUE DO
        FETCH my_cursor INTO variable1, variable2;
        IF @@SQLSTATUS <> 0 THEN
            LEAVE FETCH_LOOP;
        END IF;

        SET result = CONCAT(result, 'Column 1: ', variable1, ', Column 2: ', variable2, '\n');
    END WHILE;

    CLOSE my_cursor;

    RETURN result;
END;

-- Use a trigger
DELIMITER //
CREATE TRIGGER trigger_name BEFORE/AFTER INSERT/UPDATE/DELETE ON table_name
FOR EACH ROW
BEGIN
    -- Trigger logic here
END;
//

-- Start a transaction
START TRANSACTION;

-- Commit the transaction
COMMIT;

-- Rollback
ROLLBACK;
