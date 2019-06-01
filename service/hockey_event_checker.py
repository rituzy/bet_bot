"""Check hockey games"""
import logging
from service.hockey_game_stats import HockeyGameStats
from service.checker import Checker


class CheckerImpl(Checker):
    """Check hockey games"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_all(
            self, game_stat, total_b_koef_2per_threshold_2per,
            total_score_all_2per, is_zero_score_last_period_2per,
            total_b_koef_3per_threshold_3per, total_score_all_3per,
            is_zero_score_last_period_3per
    ) -> bool:
        """main check function combines all checks"""
        next_total_b_value = game_stat.get_match_total() + 0.5
        self.logger.debug('%s next_total_b_value %s', game_stat.game, str(next_total_b_value))
        check_2_per_result = self.check_2_period(
            game_stat, total_b_koef_2per_threshold_2per, 0.5,
            total_score_all_2per, is_zero_score_last_period_2per
        )
        self.logger.debug(
            'game : %s . 2 period check result: %s', game_stat.game, check_2_per_result
        )

        check_match_result = self.check_3_period(
            game_stat, total_b_koef_3per_threshold_3per, next_total_b_value,
            total_score_all_3per, is_zero_score_last_period_3per
        )
        self.logger.debug('game : %s . match check result: %s', game_stat.game, check_match_result)

        to_return = check_2_per_result or check_match_result

        return to_return

    def check_2_period(
            self, game_stat, total_b_koef_threshold, total_b_value, total_score_all,
            is_zero_score_last_period
    ) -> bool:
        """Check 2-d period events"""
        return self._check(game_stat, 1, total_b_koef_threshold, total_b_value,
                           game_stat.game.total_b_period2, total_score_all,
                           is_zero_score_last_period
                           )

    def check_3_period(
            self, game_stat, total_b_koef_threshold, total_b_value, total_score_all,
            is_zero_score_last_period
    ) -> bool:
        """Check 3-d period events"""
        return self._check(game_stat, 2, total_b_koef_threshold, total_b_value,
                           game_stat.game.total_b_match, total_score_all,
                           is_zero_score_last_period
                           )

    def _check(self, game_stat, periods_passed_number, total_b_koef_threshold,
               total_b_value, totals, total_score_all, is_zero_score_last_period
               ) -> bool:
        check_periods = self._check_periods_passed(periods_passed_number, game_stat)
        check_koef = self._check_koef(total_b_koef_threshold, total_b_value, totals)
        check_score_last_period = \
            self._check_score_last_period(is_zero_score_last_period, game_stat)

        self.logger.debug('game : %s . check_periods: %s', game_stat.game, check_periods)
        self.logger.debug('game : %s . check_koef: %s', game_stat.game, check_koef)
        self.logger.debug(
            'game : %s . check_score_last_period: %s', game_stat.game, check_score_last_period
        )

        return check_periods \
               and check_koef \
               and check_score_last_period

    def _check_periods_passed(self, periods_passed_number: int, game_stat: HockeyGameStats) -> bool:
        """Checks if enough periods passed according to requirements"""
        if periods_passed_number is not None \
                and periods_passed_number > int(game_stat.get_current_period_number()):
            self.logger.debug('game %s : Too few periods passed!', game_stat.game)
            return False
        return True

    def _check_koef(self, total_b_koef_threshold, total_b_value, totals):
        """Checks if koefficient is higher than threshold"""
        if total_b_koef_threshold is None \
                or total_b_value is None \
                or totals is None \
                or total_b_value not in totals \
                or totals.get(total_b_value) is None:
            self.logger.debug(
                'Value koef %s : Koef, threashold is not set or total_value '
                'is not in stats or totals is None!',
                str(total_b_value)
            )
            return False

        if total_b_koef_threshold > float(totals.get(total_b_value)):
            self.logger.debug('Value koef %s : Koef is less than desired!', str(total_b_value))
            return False
        return True

    def _check_total_score_match(self, total_score_all, game_stat):
        """Checks if total for match is lower than threshold"""
        if total_score_all is None:
            self.logger.debug('game %s : Total score is not set!', game_stat.game)
            return False
        if total_score_all <= game_stat.get_match_total():
            self.logger.debug('game %s : Total score is more than set', game_stat.game)
            return False
        return True

    def _check_score_last_period(self, is_zero_score_last_period, game_stat):
        """Checks if last period score is 0-0"""
        if is_zero_score_last_period is None:
            self.logger.debug(
                'game %s : Flag of zero score for last period is not set!', game_stat.game
            )
            return False

        if game_stat.get_last_period_total() is None:
            self.logger.debug(
                'game %s : Last period total is None: assume it''s zero!', game_stat.game
            )
            return True

        if is_zero_score_last_period is True and game_stat.get_last_period_total() > 0:
            self.logger.debug(
                'game %s : Zero last period but last period is not zero total', game_stat.game
            )
            return False
        return True
