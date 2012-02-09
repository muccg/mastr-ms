
-- Sets all the users that are Administrators in LDAP Django superusers.
-- To be run on the LIVE DB

BEGIN;


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'sdayalan@unimelb.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'selenium-noreply@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'ntakayama@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'u.roessner@unimelb.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'moshea@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'bpower@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'andrew@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'aahunter@gmail.com';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'aharvey@ccg.murdoch.edu.au';


UPDATE auth_user
    SET is_superuser = true
    WHERE username = 'tszabo@ccg.murdoch.edu.au';


COMMIT;
