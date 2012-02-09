CREATE TABLE "repository_instrumentmethod" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "method_path" text NOT NULL,
    "method_name" varchar(255) NOT NULL,
    "version" varchar(255) NOT NULL,
    "created_on" date NOT NULL,
    "creator_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "template" text NOT NULL
)
;
ALTER TABLE "repository_experiment" ADD COLUMN "instrument_method_id" integer REFERENCES "repository_instrumentmethod" ("id") DEFERRABLE INITIALLY DEFERRED;
