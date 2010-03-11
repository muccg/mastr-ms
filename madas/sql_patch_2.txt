CREATE TABLE "repository_project" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "description" text,
    "created_on" date NOT NULL,
    "client_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;

ALTER table repository_experiment add column project_id integer references repository_project ("id") deferrable initially deferred;

alter table repository_sampletimeline drop column taken_at;
alter table repository_sampletimeline drop column taken_on;
alter table repository_sampletimeline add column timeline varchar(255);

insert into repository_project (title, description, created_on) values ('Legacy project', 'Old experiments not attributed to a project are grouped here', NOW());

update repository_experiment set project_id  = 1;