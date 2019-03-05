"""Direct request from web"""
import requests
from service.parse.web.request import Request


class DirectRequest(Request):
    """Direct request from web"""
    def get(self, link):
        """reuqest from site"""
        return requests.get(link)
