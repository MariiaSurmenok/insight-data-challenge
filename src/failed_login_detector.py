"""
Implementation of feature 4:
detect patterns of three consecutive failed login attempts over
20 seconds in order to block all further attempts to reach the site
from the same IP address for the next 5 minutes.
Each attempt that would have been blocked should be written
to a log file named blocked.txt.
"""

import src.features


class AccessBlocker():
    """
    Implements detection of failed login and keep track
    of blocked users requests.

    Two class variables:
        blocked_users (dict): key (str)- user ip,
                              value (datetime) - end of blocking.
        candidates (dict): key (str) - user ip,
                           value (list) - list of datetime of at most
                           3 failed attempts to login.
    """

    def __init__(self):
        """
        Initialize attributes to keep track of users login attempts.
        """
        self.blocked_users = {}
        self.candidates = {}

    def check_request(self, request):
        """
        Check user request and decide whether user already blocked, should be blocked,
        or added to a list of the candidates on block.
        """
        if request["ip"] in self.blocked_users:
            pass

        if request["url"] == "/login" and request["ip"] not in self.blocked_users:
            pass
