alter table repository_run_samples add column vial_number integer;
alter table repository_sampleclass add column is_standards_class boolean not null default false;
CREATE TABLE "repository_instrumentsop" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "enabled" boolean NOT NULL,
    "split_threshhold" integer CHECK ("split_threshhold" >= 0) NOT NULL,
    "split_size" integer CHECK ("split_size" >= 0) NOT NULL
)
;