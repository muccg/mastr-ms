BEGIN;
CREATE TABLE "repository_clientfile" (
    "id" serial NOT NULL PRIMARY KEY,
    "experiment_id" integer NOT NULL REFERENCES "repository_experiment" ("id") DEFERRABLE INITIALLY DEFERRED,
    "filepath" text NOT NULL,
    "downloaded" boolean NOT NULL,
    "sharetimestamp" timestamp with time zone NOT NULL,
    "sharedby_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
COMMIT;
