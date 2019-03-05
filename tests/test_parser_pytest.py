import testtools
from requests_mock.contrib import fixture

from service.parse.parser import Parser

parser = Parser()


class MyTestCase(testtools.TestCase):

    TS_URL = parser.get_ts_link()
    VERSION_URL = 'https://betcity.ru/version.json?&ts=123'

    def setUp(self):
        super(MyTestCase, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())
        self.requests_mock.register_uri(
            'GET', self.TS_URL, text='{"reply":{"ts":1549436573,"dc":0},"ok":true,"lng":0,"tnow":1549436573}'
        )
        self.requests_mock.register_uri(
            'GET', self.VERSION_URL, text='{"version":71}'
        )

    @staticmethod
    def test_parse_csn():
        assert (parser.csn == 'ooca9s')

    @staticmethod
    def test_parse_ts():
        ts = parser.get_ts()
        assert(ts is not None)
        assert(isinstance(ts, int))

    @staticmethod
    def test_parse_version():
        version = parser. _get_version(123)
        assert(version is not None)
        assert(isinstance(version, int))
        assert (version == 71)
#
# def test_parse_events():
#     events = parser.get_events()
#     assert(events is not None)
#     print(events)
#
# def test_main_parse():
#     parser.parse()