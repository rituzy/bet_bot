"""Database persisting"""
import pymysql

class Saver:
    """Database persisting class"""

    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.db = None

    def save(self, game):
        """save to db"""
        self._open()

        game.translit()
        sql = """insert into hockey_game (
        game_name, game_time, period_scores, score, totals_more_2_period, totals_more_match
        ) values ('{} - {}', '{}', '{}', '{}','{}','{}')""".format(
            game.name_ht, game.name_at, game.current_time, game.periods_scores,
            game.score_match, game.total_b_period2, game.total_b_match
        )

        self._execute(sql)

        self._close()

    def _open(self):
        """open db connection"""
        self.db = pymysql.connect(self.host, self.username, self.password, self.database)

    def _execute(self, sql):
        """execute statement againts db"""
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def _close(self):
        """close db connection"""
        self.db.close()
