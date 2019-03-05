"""Sender interface"""
import transliterate


class Sender:
    """Sender interface"""
    def send(self, bot_address_to_send, chat_id, action):
        """send a message"""


    @staticmethod
    def urlify(in_string):
        """translate russian letters string to string of latin letters"""
        return transliterate.translit("_".join(in_string.split()), reversed=True)
