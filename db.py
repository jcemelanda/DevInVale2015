# coding: utf-8

import sqlite3


class DB(object):

    def __init__(self, database):
        self.connection = None
        self.database = database
        self._create_score_table()

    def _connect(self):
        self.connection = sqlite3.connect(self.database)

    def _create_score_table(self):
        self._connect()

        with self.connection as con:
            try:
                con.execute('CREATE TABLE scores (score INTEGER, player TEXT)')
            except sqlite3.OperationalError:
                pass
        self.connection.close()

    def save_score(self, score, player):
        values = (score, player, )

        self._connect()
        with self.connection as con:
            con.execute("INSERT INTO scores VALUES (?, ?)", values)

        self.connection.close()

    def get_scores(self, player):
        values = (player, )
        self._connect()
        scores = None
        with self.connection as con:
            scores = con.execute(
                "SELECT * FROM scores where player=?", values).fetchmany(size=10)

        self.connection.close()

        return scores
