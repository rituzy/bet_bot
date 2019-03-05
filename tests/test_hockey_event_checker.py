from dto.hockey_game import HockeyGame
from service.hockey_game_stats import HockeyGameStats
from service.hockey_event_checker import HockeyEventChecker


name_ht, name_at, current_time, score, total_b_match, total_b_period2 \
    = "team_home", "team_guest", "2-abracadabra", {
            "main":[[4, 2]],
            "ext" :[[3, 1], [1, 1]]
}, {6.5: 1.15, 7: 1.28, 8: 2.75, 8.5: 3.8, 9.5: 7.8},\
      {0.5: 1.11, 1.5: 1.55, 2.5: 2.75}
gameStats = HockeyGameStats(HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2))
gameStats.calculate()


def test_check_periods_passed():
    assert(HockeyEventChecker._check_periods_passed(2, gameStats) is True)
    assert(HockeyEventChecker._check_periods_passed(3, gameStats) is False)


def test_check_koef_match():
    totals = gameStats.game.total_b_match
    assert(HockeyEventChecker._check_koef(1.2, 7, totals) is True)
    assert(HockeyEventChecker._check_koef(1.3, 7, totals) is False)
    assert(HockeyEventChecker._check_koef(1.3, 2, totals) is False)
    assert(HockeyEventChecker._check_koef(1.3, None, totals) is False)
    assert(HockeyEventChecker._check_koef(None, None, totals) is False)


def test_check_total_score_match():
    assert(HockeyEventChecker._check_total_score_match(None, gameStats) is False)
    assert(HockeyEventChecker._check_total_score_match(3, gameStats) is False)
    assert(HockeyEventChecker._check_total_score_match(8, gameStats) is True)


def test_check_score_last_period():
    assert(HockeyEventChecker._check_score_last_period(None, gameStats) is False)
    assert(HockeyEventChecker._check_score_last_period(True, gameStats) is False)
    assert(HockeyEventChecker._check_score_last_period(False, gameStats) is True)