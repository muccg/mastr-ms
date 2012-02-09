BEGIN;

-- Add the new completeness column and associated index.
ALTER TABLE "repository_run_samples" ADD COLUMN "complete" BOOLEAN NOT NULL DEFAULT 'f';
CREATE INDEX "repository_run_samples_complete" ON "repository_run_samples" ("complete");

ALTER TABLE "repository_run" ADD COLUMN "state" SMALLINT NOT NULL DEFAULT 0;
ALTER TABLE "repository_run" ADD COLUMN "sample_count" INTEGER NOT NULL DEFAULT 0;
ALTER TABLE "repository_run" ADD COLUMN "incomplete_sample_count" INTEGER NOT NULL DEFAULT 0;
ALTER TABLE "repository_run" ADD COLUMN "complete_sample_count" INTEGER NOT NULL DEFAULT 0;
CREATE INDEX "repository_run_state" ON "repository_run" ("state");

COMMIT;
