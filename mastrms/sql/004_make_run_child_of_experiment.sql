BEGIN;

ALTER TABLE "repository_run"
    ADD COLUMN "experiment_id" integer REFERENCES "repository_experiment" ("id") DEFERRABLE INITIALLY DEFERRED;


UPDATE repository_run SET experiment_id = ids.experiment_id
FROM (
    SELECT DISTINCT 
        e.id AS experiment_id, 
        r.id AS run_id 
    FROM repository_run r 
                JOIN repository_run_samples rs ON r.id = rs.run_id 
                JOIN repository_sample s ON rs.sample_id = s.id 
                JOIN repository_experiment e ON e.id = s.experiment_id ) AS ids
WHERE repository_run.id = ids.run_id;

COMMIT;
