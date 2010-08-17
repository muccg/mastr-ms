alter table repository_run_samples add column vial_number integer;
alter table repository_sampleclass add column is_standards_class boolean not null default false;