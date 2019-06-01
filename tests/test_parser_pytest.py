import mock
import testtools

from service.parse.parser import Parser


class ParserTest(testtools.TestCase):

    def setUp(self):
        super(ParserTest, self).setUp()
        self.parser = Parser(None)

    @mock.patch('service.parse.parser.Parser.get_ts', return_value=123)
    def test_parse_ts(self, get_ts_function):
        ts = self.parser.get_ts()
        assert(ts is not None)
        assert(isinstance(ts, int))

    @mock.patch('service.parse.parser.Parser._get_version', return_value=345)
    def test_parse_version(self, get_version_function):
        version = self.parser._get_version(123)
        assert(version is not None)
        assert(isinstance(version, int))
        assert (version == 345)
#
# def test_parse_events():
#     events = parser.get_events()
#     assert(events is not None)
#     print(events)
#
# def test_main_parse():
#     parser.parse()