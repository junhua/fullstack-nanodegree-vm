#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def execute(command):
    conn = connect()
    c = conn.cursor()

    c.execute(command)

    conn.commit()
    conn.close()

    return conn


def execute_with_output(command):
    conn = connect()
    c = conn.cursor()

    c.execute(command)

    conn.commit()
    result = c.fetchall()
    conn.close()

    return result


def deleteMatches():
    """Remove all the match records from the database."""

    execute("DELETE FROM Matches")


def deletePlayers():
    """Remove all the player records from the database."""
    execute("DELETE FROM Players")


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) from Players;")
    conn.commit()

    result = c.fetchone()[0]

    conn.close()

    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """

    # execute("INSERT INTO Players(uid, name) VALUES (DEFAULT,'%s');"%name)
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO Players(uid, name) VALUES (DEFAULT,%s)", (name,))

    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches)
    """

    result = execute_with_output("""
        select * from Standings
        """)

    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args: winner, loser
    """
    execute("INSERT INTO Matches (winner,loser) VALUES(%s,%s)" %
            (winner, loser,))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.


    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
    """

    players = [(row[0], row[1]) for row in playerStandings()]

    assert len(players) >= 2, "Need more than 2 players to make a pair"
    assert len(
        players) % 2 == 0, "Need even number of players to make pairs, assuming no walk-over"

    pairings = zip(players[0::2], players[1::2])

    # flatten the pairings and convert back to a tuple
    results = [tuple(list(sum(pairing, ()))) for pairing in pairings]

    return results
