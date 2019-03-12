"""Main script to run the app"""
import time
from service.hockey_game_stats import HockeyGameStats
from service.hockey_event_checker import HockeyEventChecker
from service.parse.parser import Parser
from send.telegram_sender_impl import TelegramSender
from service.parse.web.tor_request_impl import TorRequest
from dao.mysql_db import Saver
import config.config_data as conf


class Runner:
    """Main script to run the app"""
    def __init__(self, checker, request) -> None:
        self.sender = TelegramSender()
        self.bot_address = conf.BOT_ADDRESS
        self.bot_chat_id = conf.BOT_CHAT_ID
        self.sleep_delay = conf.SLEEP_DELAY
        self.total_b_kef_per2 = conf.TOTAL_B_KEF_PER2
        self.total_score_all_2per = conf.TOTAL_SCORE_ALL_2PER
        self.is_zero_score_per2 = conf.IS_ZERO_SCORE_PER2
        self.total_b_kef_match = conf.TOTAL_B_KEF_MATCH
        self.total_score_all_match = conf.TOTAL_SCORE_ALL_MATCH
        self.is_zero_score_match = conf.IS_ZERO_SCORE_MATCH
        self._request = request
        self.saver = Saver(conf.DB_HOST, conf.DB_USERNAME, conf.DB_PASSWORD, conf.DATABASE)

    def run(self):
        """Main function to run the app"""
        parser = Parser(self._request)
        while True:
            game_stats = [HockeyGameStats(g) for g in parser.parse()]
            checker = HockeyEventChecker()
            for game_stat in game_stats:
                game_stat.calculate()
                result = checker.check_all(
                                            game_stat,
                                            self.total_b_kef_per2,
                                            self.total_score_all_2per,
                                            self.is_zero_score_per2,
                                            self.total_b_kef_match,
                                            self.total_score_all_match,
                                            self.is_zero_score_match
                                           )
                cur_game = str(game_stat.game.url_repr())
                if result:
                    self.sender.send(self.bot_address, self.bot_chat_id,
                                     cur_game.format(' is ready for betting!')
                                     )
                    self.saver.save(game_stat.game)

            time.sleep(self.sleep_delay)


if __name__ == "__main__":
    import logging
    from logging.handlers import RotatingFileHandler

    # logging section
    # 10 - DEBUG level
    # 20 - INFO level
    # 30 - WARNING level
    # 40 - ERROR level
    # 50 - FATAL level
    LOG_LEVEL = 10
    LOG_FILE = 'hockey_event.log'
    logging.getLogger().setLevel(int(LOG_LEVEL))
    HANDLER = RotatingFileHandler(LOG_FILE, maxBytes=10000000, backupCount=10)
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    HANDLER.setFormatter(FORMATTER)
    logging.getLogger().addHandler(HANDLER)

    runner = Runner(HockeyEventChecker, TorRequest)
    runner.run()
