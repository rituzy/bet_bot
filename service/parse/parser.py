"""Parser for data from bet site"""
import logging
import requests
from dto.hockey_game import HockeyGame

class Parser:
    """Parser for data from bet site"""
    PERIODS_RESULTS_TITLE = "\u0418\u0441\u0445\u043e\u0434\u044b \u043f\u043e \u043f\u0435" \
                            "\u0440\u0438\u043e\u0434\u0430\u043c"
    SECOND_PERIOD_TITLE = "2-\u0439 \u043f\u0435\u0440\u0438\u043e\u0434"
    HOCKEY_TITLE = "\u0422\u043e\u0442\u0430\u043b"

    def __init__(self, request):
        self.csn = 'ooca9s'
        self.ts_link = 'https://ad.betcity.ru/d/settings/ts?csn={}'
        self.version_link = 'https://betcity.ru/version.json?&ts={}'
        self.events_link = 'https://ad.betcity.ru/d/on_air/events?rev=6&ver={}'
        self.event_details_link = 'https://ad.betcity.ru/d/on_air/bets?rev=7&ids={}&ver={}'
        self.logger = logging.getLogger(__name__)
        self._request = request

    def parse(self):
        """main function to be used for parsing site and returns array of games detailed"""
        games = []
        try:
            events = self._get_event_elements(
                self._get_events(),
                'name_sp',
                "\u0425\u043e\u043a\u043a\u0435\u0439"
            )
            self._get_games_data(events, self.get_version(), games)
        except requests.exceptions.Timeout:
            self.logger.error('time out on getting data from site')
        except requests.exceptions.TooManyRedirects:
            self.logger.error('too many redirects on getting data from site')
        except requests.exceptions.RequestException as e:
            self.logger.fatal('Fatal exception on getting data from site: %s', str(e))

        return games

    def get_ts_link(self) -> str:
        """Get the link for timestamp receiving"""
        return self.ts_link.format(self.csn)

    def get_ts(self) -> int:
        """Get timestamp"""
        result_ts = self._request.get(self, self.get_ts_link())
        try:
            response_dict = result_ts.json()
        except ValueError:
            return 0
        return response_dict.get("reply").get("ts")

    def get_version(self) -> int:
        """Get version number"""
        return self._get_version(self.get_ts())

    def _get_version(self, time_stamp) -> int:
        """Get version number by timestamp"""
        result_version = self._request.get(self, self._get_version_link(time_stamp))
        try:
            response_dict = result_version.json()
        except ValueError:
            return 0
        return response_dict.get("version")

    def _get_version_link(self, time_stamp) -> str:
        """Get the link for version receiving"""
        return self.version_link.format(time_stamp)

    def _get_events(self):
        """Get all game events' titles"""
        version = self.get_version()
        self.version_link = self.version_link.format(version)
        result_events = self._request.get(self, self.events_link.format(version))
        try:
            response_dict = result_events.json()
        except ValueError:
            return []
        return response_dict.get("reply").get("sports")

    @staticmethod
    def _get_event_elements(json_text, key_name, value_name):
        """Get all game events' titles in array"""
        to_return = []
        for root_element in json_text:
            if value_name in json_text.get(root_element).get(key_name):
                current_event_element = json_text.get(root_element)
                to_return.append(current_event_element)
        return to_return

    def _get_games_data(self, events, version, games):
        """Put details for all events and put them to games"""
        for current_event in events:
            for chmp_id in current_event.get("chmps"):
                for event_id in current_event.get("chmps").get(chmp_id).get("evts"):
                    self._get_game_details(event_id, version, games)

    def _get_game_details(self, event_id, version, result_games):
        """Prepare details for current event and put them to games"""
        name_ht, name_at, current_time, score, total_b_match, total_b_period2 =\
            None, None, None, None, dict(), dict()

        event_details_link = self.event_details_link.format(event_id, version)

        result_events = self._request.get(self, event_details_link)

        try:
            events = result_events.json().get("reply").get("sports")
        except ValueError:
            return

        if events is None:
            return

        for root_id in events:
            for chmp_id in events.get(root_id).get("chmps"):
                for current_event_id in events.get(root_id).get("chmps").get(chmp_id).get("evts"):
                    game_details = events.get(root_id).get("chmps")\
                        .get(chmp_id).get("evts").get(current_event_id)
                    current_time = game_details.get("time_name")
                    name_ht = game_details.get("name_ht")
                    name_at = game_details.get("name_at")
                    score = game_details.get("sc_ev_cmx")
                    game_stats = game_details.get("ext")
                    if game_stats is not None:
                        for stat_id in game_stats:
                            cur_stat = game_stats.get(stat_id)
                            if cur_stat.get("name") == self.HOCKEY_TITLE:
                                for total_id in cur_stat.get("data"):
                                    total_element = cur_stat.get("data")\
                                        .get(total_id).get("blocks").get("T")
                                    if total_element is not None:
                                        total_b_match[total_element.get("Tot")] = \
                                            total_element.get("Tb").get("kf")
                            if cur_stat.get("name") == self.PERIODS_RESULTS_TITLE:
                                for total_per_id in cur_stat.get("rows"):
                                    total_per_element = cur_stat.get("rows").get(total_per_id)
                                    if self.SECOND_PERIOD_TITLE == total_per_element.get("name"):
                                        match_total_data = total_per_element.get("data")
                                        for total_per_id_sub_id in match_total_data:
                                            tags = ["T{}".format(i) for i in range(1, 10)]
                                            cur_total_period_result = \
                                                [match_total_data.get(total_per_id_sub_id)
                                                 .get("blocks").get(tag) for tag in tags]
                                            for cur_per in cur_total_period_result:
                                                if cur_per is not None:
                                                    total_b_period2[cur_per.get("Tot")] =\
                                                        cur_per.get("Tb").get("kf")
        result_games.append(
            HockeyGame(name_ht, name_at, current_time, score, total_b_match, total_b_period2)
        )
