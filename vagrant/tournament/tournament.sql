-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop previous DB, create a new db and connects

Drop database if exists tournament;
Create database tournament;
\connect tournament;

-- players table: name and id
Create table players(
  id Serial primary key,
  name text
);

-- matches table: id, winner, loser
Create table matches(
  id Serial primary key,
  winner Integer references players(id),
  loser Integer references players(id)
);
-- Player standings view:
Create view player_standings As
  Select
    players.id,
    players.name,
    (Select count(*) From matches where players.id = matches.winner) as wins,
    (Select count(*) From matches where players.id = matches.winner or players.id = matches.loser) as matches
  From players
  Order by wins desc;
