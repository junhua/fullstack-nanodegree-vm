-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players (
	uid			SERIAL PRIMARY KEY,
	name		VARCHAR(40)
);


CREATE TABLE Matches (
	id			serial primary key,
	p1			integer REFERENCES Players (uid),
	p2			integer REFERENCES Players (uid),
	winner		integer REFERENCES Players (uid),
	loser		integer REFERENCES Players (uid)
);

-- Count number of wins

CREATE VIEW WinCounts AS
SELECT Players.uid, Players.name, COUNT(Matches.winner) AS wins 
FROM Players LEFT JOIN Matches
ON Players.uid = Matches.winner
GROUP BY Players.uid;

-- Total matches

CREATE VIEW TotalMatches AS
SELECT Players.uid, Players.name, COUNT(Matches.id) AS total_matches 
FROM Players LEFT JOIN Matches
ON Players.uid = Matches.p1 OR Players.uid = Matches.p2
GROUP BY Players.uid;

-- satndings

CREATE VIEW Standings AS
    SELECT WinCounts.uid, WinCounts.name, wins, total_matches 
    FROM WinCounts LEFT JOIN TotalMatches
    ON WinCounts.uid = TotalMatches.uid
    ORDER BY wins desc;

