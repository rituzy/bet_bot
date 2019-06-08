"""HockeyGame decorator for gathering statistics"""


class HockeyGameStats:
    """HockeyGame decorator for gathering statistics"""
    def __init__(self, game):
        self.game = game
        self.match_total = None

    def calculate(self):
        """Logic to figure out the game statistics"""
        try:
            self.match_total = sum(self.game.score_match) if self.game.score_match is not None else None
        except TypeError:
            self.match_total = None

    def get_last_period_total(self):
        """Get total for last period"""
        return sum(self.game.periods_scores[-1]) \
            if self.game.periods_scores is not None and self.game.periods_scores else None

    def get_current_period_number(self):
        """Get current period number"""
        return len(self.game.periods_scores) \
            if self.game is not None and self.game.periods_scores is not None else 0

    def get_match_total(self):
        """Get total for the match"""
        return self.match_total
