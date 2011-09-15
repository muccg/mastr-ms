BEGIN;

-- I don't know when and how this UNIQUE constraint was added, but it does not match the current sqlall output
ALTER TABLE repository_run_samples DROP constraint repository_run_samples_run_id_key;

ALTER TABLE repository_run_samples ADD COLUMN method_number integer CHECK("method_number" >= 0);

COMMIT;
