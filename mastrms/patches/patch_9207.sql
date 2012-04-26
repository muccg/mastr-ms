begin;

alter table repository_animalinfo alter column sex drop not null;
alter table repository_animalinfo alter column parental_line drop not null;

commit;