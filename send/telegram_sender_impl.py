"""Sending messages to telegram bot"""
import logging
import urllib.request as req

from send.sender import Sender


class TelegramSender(Sender):
    """Telegram sender class encapsulates sending details"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send(self, bot_address_to_send, chat_id, action):
        if action is None or bot_address_to_send is None:
            return

        for cid in chat_id:
            bot_address_to_send_current = bot_address_to_send \
                                          + cid + '&action=' + self.urlify(action)
            self.logger.debug(bot_address_to_send_current)
            try:
                conn = req.urlopen(bot_address_to_send_current)
                return_str = str(conn.read())
                self.logger.debug('Return code from the sending page: %s', str(conn.getcode()))
                self.logger.debug('Return message result from the sending page: %s',
                                  return_str.split('Result :', 1)[1].split('!\n\t\t</div>', 1)[0])
            except HTTPError:
                self.logger.error('Could not send to telegram!')

