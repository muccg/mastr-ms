BEGIN;

-- I don't know when and how this UNIQUE constraint was added, but it does not match the current sqlall output
ALTER TABLE repository_run_samples DROP CONSTRAINT repository_run_samples_run_id_key;

ALTER TABLE repository_run_samples ADD COLUMN method_number integer CHECK("method_number" >= 0);

-- We are dropping RunRuleGenerator and add Number of Methods and Order of Methods on the Run itself

ALTER TABLE repository_run DROP CONSTRAINT "rule_generator_id_refs_id_e064e1f3";
DROP TABLE repository_runrulegenerator;

ALTER TABLE repository_run ADD CONSTRAINT "rule_generator_id_refs_id_f4ced915" FOREIGN KEY("rule_generator_id") REFERENCES "repository_rulegenerator" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE repository_run ADD COLUMN number_of_methods integer;
ALTER TABLE repository_run ADD COLUMN order_of_methods integer;

COMMIT;

