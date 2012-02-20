ALTER TABLE repository_run_samples ADD COLUMN "filename" VARCHAR(255);
ALTER TABLE repository_run ADD COLUMN "generated_output" TEXT;