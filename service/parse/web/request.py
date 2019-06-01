"""Request from web interface"""
import abc

class Request(metaclass=abc.ABCMeta):
    """Request from web interface"""

    @abc.abstractmethod
    def get(self, link):
        """request from site"""
        pass
