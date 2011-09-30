BEGIN;

ALTER TABLE repository_rulegenerator ADD COLUMN node VARCHAR(255);

COMMIT;

