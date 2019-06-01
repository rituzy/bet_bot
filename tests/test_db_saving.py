import mock
import testtools

from dao.mysql_db import Saver
from dto.hockey_game import HockeyGame
from service.hockey_game_stats import HockeyGameStats


class SenderTest(testtools.TestCase):

    def setUp(self):
        super(SenderTest, self).setUp()
        name_ht, name_at, current_time, score, total_b_match, total_b_period2 \
            = "team_home", "team_guest", "2-abracadabra", {
            "main": [[4, 2]],
            "ext": [[3, 1], [1, 1]]
        }, {6.5: 1.15, 7: 1.28, 8: 2.75, 8.5: 3.8, 9.5: 7.8}, \
              {0.5: 1.11, 1.5: 1.55, 2.5: 2.75}
        self.game_stat = HockeyGameStats(
            HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2))

    @mock.patch('dao.mysql_db.Saver.save')
    def test_db_save(self, save_function):
        saver = Saver("host", "root", "secret", "dbname")
        saver.save(self.game_stat)
