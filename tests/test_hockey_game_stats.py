import testtools

from dto.hockey_game import HockeyGame
from service.hockey_game_stats import HockeyGameStats


class GameStatsTotalTests(testtools.TestCase):

    def setUp(self):
        super(GameStatsTotalTests, self).setUp()
        name_ht, name_at, current_time, score, total_b_match, total_b_period2 \
            = "team_home", "team_guest", "2-abracadabra", {
            "main": [[4, 2]],
            "ext": [[3, 1], [1, 1]]
        }, {6.5: 1.15, 7: 1.28, 8: 2.75, 8.5: 3.8, 9.5: 7.8}, \
              {0.5: 1.11, 1.5: 1.55, 2.5: 2.75}
        self.game_stat = HockeyGameStats(
            HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2))
        self.game_stat.calculate()

    def test_match_total(self):
        assert (self.game_stat.get_match_total() != 0)
        assert (self.game_stat.get_match_total() == 6)

    def test_last_period_total(self):
        assert (self.game_stat.get_last_period_total() != 0)
        assert (self.game_stat.get_last_period_total() == 2)

    def test_last_period_number(self):
        assert (self.game_stat.get_current_period_number() == 2)
