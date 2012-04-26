BEGIN;

ALTER TABLE "repository_instrumentmethod" ADD COLUMN "randomisation" boolean NOT NULL DEFAULT false;
ALTER TABLE "repository_instrumentmethod" ADD COLUMN "blank_at_start" boolean NOT NULL DEFAULT false;
ALTER TABLE "repository_instrumentmethod" ADD COLUMN "blank_at_end" boolean NOT NULL DEFAULT false;
ALTER TABLE "repository_instrumentmethod" ADD COLUMN "blank_position" varchar(255);
ALTER TABLE "repository_instrumentmethod" ADD COLUMN "obsolete" boolean NOT NULL DEFAULT false;
ALTER TABLE "repository_instrumentmethod" ADD COLUMN "obsolescence_date" date;

CREATE TABLE "repository_run" (
    "id" serial NOT NULL PRIMARY KEY,
    "method_id" integer NOT NULL REFERENCES "repository_instrumentmethod" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_on" date NOT NULL,
    "creator_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(255)
)
;
CREATE TABLE "repository_run_samples" (
    "id" serial NOT NULL PRIMARY KEY,
    "run_id" integer NOT NULL REFERENCES "repository_run" ("id") DEFERRABLE INITIALLY DEFERRED,
    "sample_id" integer NOT NULL REFERENCES "repository_sample" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("run_id", "sample_id")
)
;
COMMIT;

BEGIN;

ALTER TABLE "repository_biologicalsource" ADD COLUMN "abbreviation" varchar(5);
ALTER TABLE "repository_treatment" ADD COLUMN "abbreviation" varchar(5);
ALTER TABLE "repository_sampletimeline" ADD COLUMN "abbreviation" varchar(5);
ALTER TABLE "repository_organ" ADD COLUMN "abbreviation" varchar(5);

ALTER TABLE "mdatasync_server_nodeclient" ADD COLUMN "default_data_path" varchar(255);
ALTER TABLE "repository_run" ADD COLUMN     "machine_id" integer REFERENCES "mdatasync_server_nodeclient" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;