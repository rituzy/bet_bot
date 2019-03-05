import pytest
import testtools
from send.telegram_sender_impl import TelegramSender
from requests_mock.contrib import fixture

SENDER = TelegramSender()

class SenderTest(testtools.TestCase):

    SEND_URL = 'http://izutov.herokuapp.com/out_of_office/?chat_id='
    CHAT_ID = ['123']
    ACTION = 'Русский текст'

    def setUp(self):
        super(SenderTest, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())
        self.requests_mock.register_uri(
            'GET', self.SEND_URL, text='ok'
        )

    def test_snd(self):
        try:
            SENDER.send(self.SEND_URL, self.CHAT_ID, self.ACTION)
        except Exception:
            pytest.fail("Exception is not expected on sending the message to telegram")
