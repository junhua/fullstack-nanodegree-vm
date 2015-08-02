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

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

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

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    result = execute_with_output("""
        select * from Standings
        """)

    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    execute("INSERT INTO Matches (p1,p2,winner,loser) VALUES(%s,%s,%s,%s)" %
            (winner, loser, winner, loser,))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    players = [(row[0], row[1]) for row in playerStandings()]

    assert len(players) >= 2, "Need more than 2 players to make a pair"
    assert len(
        players) % 2 == 0, "Need even number of players to make pairs, assuming no walk-over"

    pairings = zip(players[0::2], players[1::2])

    # flatten the pairings and convert back to a tuple
    results = [tuple(list(sum(pairing, ()))) for pairing in pairings]

    return results
