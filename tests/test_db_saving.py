from dto.hockey_game import HockeyGame
from dao.mysql_db import Saver

name_ht, name_at, current_time, score, total_b_match, total_b_period2 \
    = "team_home", "team_guest", "2-abracadabra", {
    "main": [[4, 2]],
    "ext": [[3, 1], [1, 1]]
}, {6.5: 1.15, 7: 1.28, 8: 2.75, 8.5: 3.8, 9.5: 7.8}, \
      {0.5: 1.11, 1.5: 1.55, 2.5: 2.75}
game = HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2)


def test_db_save():
    saver = Saver("host", "root", "secret", "dbname")
    saver.save(game)
