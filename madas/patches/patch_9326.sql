begin;
alter table repository_sample add column sample_class_sequence smallint not null default 1;
create index repository_sample_sample_class_sequence on repository_sample (sample_class_sequence);
commit;