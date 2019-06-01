import testtools
from dto.hockey_game import HockeyGame
from service.hockey_game_stats import HockeyGameStats
from service.hockey_event_checker import CheckerImpl


class CheckerKoeffsTests(testtools.TestCase):

    def setUp(self):
        super(CheckerKoeffsTests, self).setUp()
        name_ht, name_at, current_time, score, total_b_match, total_b_period2 \
            = "team_home", "team_guest", "2-abracadabra", {
                    "main":[[4, 2]],
                    "ext" :[[3, 1], [1, 1]]
        }, {6.5: 1.15, 7: 1.28, 8: 2.75, 8.5: 3.8, 9.5: 7.8},\
              {0.5: 1.11, 1.5: 1.55, 2.5: 2.75}
        self.game_stat = HockeyGameStats(HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2))
        self.game_stat.calculate()

        self.checker = CheckerImpl()


    def test_check_periods_passed(self):
        assert(self.checker._check_periods_passed(2, self.game_stat) is True)
        assert(self.checker._check_periods_passed(3, self.game_stat) is False)


    def test_check_koef_match(self):
        totals = self.game_stat.game.total_b_match
        assert(self.checker._check_koef(1.2, 7, totals) is True)
        assert(self.checker._check_koef(1.3, 7, totals) is False)
        assert(self.checker._check_koef(1.3, 2, totals) is False)
        assert(self.checker._check_koef(1.3, None, totals) is False)
        assert(self.checker._check_koef(None, None, totals) is False)


    def test_check_total_score_match(self):
        assert(self.checker._check_total_score_match(None, self.game_stat) is False)
        assert(self.checker._check_total_score_match(3, self.game_stat) is False)
        assert(self.checker._check_total_score_match(8, self.game_stat) is True)


    def test_check_score_last_period(self):
        assert(self.checker._check_score_last_period(None, self.game_stat) is False)
        assert(self.checker._check_score_last_period(True, self.game_stat) is False)
        assert(self.checker._check_score_last_period(False, self.game_stat) is True)