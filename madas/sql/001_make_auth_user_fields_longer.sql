
-- Updates auth_user column lengths to match code in current Mango.

BEGIN;

ALTER TABLE auth_user
    ALTER COLUMN username TYPE varchar(256),
    ALTER COLUMN first_name TYPE varchar(256),
    ALTER COLUMN last_name TYPE varchar(256);

COMMIT;

