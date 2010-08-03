alter table repository_run_samples alter column sample_id drop not null;
alter table repository_run_samples add column "type" integer CHECK ("type" >= 0) NOT NULL default 0;
alter table repository_run_samples add column "sequence" integer CHECK ("sequence" >= 0) NOT NULL default 0;
update repository_run_samples set sequence = id;