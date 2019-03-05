"""DTO Hockey Game for storing game data"""


class HockeyGame:
    """DTO Hockey Game for storing game data"""

    def __init__(self, name_ht, name_at, current_time, score, total_b_match, total_b_period2):
        self.name_ht = name_ht
        self.name_at = name_at
        self.current_time = current_time

        if "main" in score and len(score["main"]) > 0:
            self.score_match = score["main"][0]
        else:
            self.score_match = []

        self.periods_scores = score["ext"] if "ext" in score else []
        self.total_b_match = total_b_match
        self.total_b_period2 = total_b_period2

    def __repr__(self) -> str:
        return \
            "{} - {}. Current time {} .Period scores {}.Score: {}." \
            "Totals for 2 period {}. Totals for match: {}" \
                .format(
                    self.name_ht, self.name_at, self.current_time, self.periods_scores,
                    self.score_match, self.total_b_period2, self.total_b_match
                )

    def url_repr(self) -> str:
        """prepare game data to send in GET request as GET with parameters"""
        to_return = "{} - {} Score: {} Score periods: {}" \
            .format(self.name_ht, self.name_at, self.score_match, self.periods_scores)
        return to_return.replace('\n', ' ').replace('\r', '')
