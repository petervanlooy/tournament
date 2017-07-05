-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
\c forum
drop database tournament;
create database tournament;
\c tournament

create table players (
    id serial primary key,
    name varchar(50) not null,
    time_created timestamp default current_timestamp,
    wins int default 0,
    matches int default 0
);

create table matches(
    id serial primary key,
    winner int references players(id),
    loser int references players(id),
    time_created timestamp default current_timestamp
);

create or replace function update_player_stats_after_inserted_match()
    returns trigger as
$BODY$
begin
    update players set matches = matches + 1, wins = wins + 1
        where id = new.winner;
    update players set matches = matches + 1
        where id = new.loser;

    return new;
end;
$BODY$
language plpgsql;

create or replace function update_player_stats_after_deleted_match()
    returns trigger as
$BODY$
begin
    update players set matches = matches - 1, wins = wins - 1
        where id = old.winner;
    update players set matches = matches - 1
        where id = old.loser;

    return new;
end;
$BODY$
language plpgsql;

create trigger tri_matches after insert on matches
    for each row
    execute procedure update_player_stats_after_inserted_match();

create trigger trd_matches after delete on matches
    for each row
    execute procedure update_player_stats_after_deleted_match();


