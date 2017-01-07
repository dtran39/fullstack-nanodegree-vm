-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop previous DB, create a new db and connects
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament;

-- players table: name and id

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT
);

-- matches table: id, winner, loser

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INT REFERENCES players(id),
  loser INT REFERENCES players(id)
);

-- Standings:
CREATE VIEW player_standings AS
	SELECT
    players.id,
		players.name,
		(SELECT COUNT(*) FROM matches WHERE players.id = matches.winner) AS wins,
		(SELECT COUNT(*) FROM matches WHERE players.id = matches.winner OR players.id = matches.loser) AS matches
	FROM players
	ORDER BY wins DESC;
