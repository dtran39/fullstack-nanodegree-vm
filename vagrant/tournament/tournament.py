#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute_sql(sql_statement, is_an_update=True, params=None):
    db_connection = connect()
    db_cursor = db_connection.cursor()
    if not params:
        db_cursor.execute(sql_statement)
    else:
        db_cursor.execute(sql_statement, params)
    result = None
    if is_an_update:
        db_connection.commit()
    else:
        result = db_cursor.fetchall()
    db_connection.close()
    return result
def execute_update(sql_statement, params=None):
    execute_sql(sql_statement, True, params)
def execute_query(sql_statement, params=None):
    return execute_sql(sql_statement, False, params)
def deleteMatches():
    """Remove all the match records from the database."""
    execute_update("Delete from matches")

def deletePlayers():
    """Remove all the player records from the database."""
    execute_update("Delete from players")

def countPlayers():
    """Returns the number of players currently registered."""
    return execute_query("SELECT COUNT(*) AS total FROM players")[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    execute_update("Insert into players (name) Values (%s)", (name,))

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
    return execute_query("Select * from player_standings")

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    return execute_update("INSERT INTO matches(winner, loser) VALUES (%s, %s)",
                          (winner, loser))

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
