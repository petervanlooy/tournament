#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteTable(table_name):
    """Remove all the records from table with table_name."""
    db = connect()
    c = db.cursor()
    c.execute('delete from {};'.format(table_name))
    db.commit()
    db.close()

def deleteMatches():
    """Remove all the match records from the database."""
    deleteTable('matches')

def deletePlayers():
    """Remove all the player records from the database."""
    deleteTable('players')

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute('select count(*) from players;')
    result = c.fetchone()[0]
    db.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute('insert into players (name) values (%s)', (bleach.clean(name), ))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()
    c.execute('select id, name, wins, matches from players order by wins desc;')
    result = c.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('insert into matches (winner, loser) values (%s, %s)', (winner, loser))
    db.commit()
    db.close()
 
 
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
    l = []
    t = tuple()
    standings = playerStandings()
    for id, name, wins, matches in standings:
        if len(t) == 4 or len(t) == 0:
            t = (id, name)
        else:
            t += (id, name)
            l.append(t)
    return l
    

