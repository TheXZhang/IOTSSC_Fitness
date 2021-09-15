drop table if exists classification;
create table classification(
    id serial PRIMARY KEY NOT NULL ,
    timestamp varchar(255),
    classification varchar(255)
);

drop table if exists achievement;
create table achievement(
    id serial PRIMARY KEY NOT NULL ,
    walking INTEGER,
    running INTEGER
);

CREATE OR REPLACE FUNCTION mytrigger()
  RETURNS trigger AS
$BODY$
begin
    PERFORM pg_notify('achievement', row_to_json(new)::text);
    return new;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE;

CREATE TRIGGER mytrigger
    AFTER INSERT OR UPDATE ON achievement
    FOR EACH ROW
    EXECUTE PROCEDURE mytrigger();