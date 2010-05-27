CREATE TABLE "repository_project_managers" (
    "id" serial NOT NULL PRIMARY KEY,
    "project_id" integer NOT NULL REFERENCES "repository_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("project_id", "user_id")
);
