"""Check games interface"""


class Checker:
    """Check games interface"""
    def check_all(
            self, game_stat, total_b_koef_2per_threshold_2per, total_b_value_2per,
            total_score_all_2per, is_zero_score_last_period_2per,
            total_b_koef_3per_threshold_3per, total_b_value_3per,
            total_score_all_3per, is_zero_score_last_period_3per
    ) -> bool:
        """main check function combines all checks"""

    def check_2_period(
            self, game_stat, total_b_koef_threshold, total_b_value,
            total_score_all, is_zero_score_last_period
    ) -> bool:
        """Check 2-d period events"""

    def check_3_period(
            self, game_stat, total_b_koef_threshold, total_b_value,
            total_score_all, is_zero_score_last_period
    ) -> bool:
        """Check 3-d period events"""
