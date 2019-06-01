"""Request from web through tor network"""
import requests
from service.parse.web.request import Request


class TorRequest(Request):
    """Request from web through tor network"""
    def get(self, link):
        """reuqest from site"""
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
        return session.get(link)
