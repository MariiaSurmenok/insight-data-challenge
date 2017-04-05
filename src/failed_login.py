"""
Implementation of feature 4:
detect patterns of three consecutive failed login attempts over
20 seconds in order to block all further attempts to reach the site
from the same IP address for the next 5 minutes.
Each attempt that would have been blocked should be written
to a log file named blocked.txt.
"""

from datetime import timedelta

from io_utils import date_formatting, read_from_file, write_information_to_file


class AccessBlocker():
    """
    Implements detection of failed login and keep track
    of blocked users requests.

    Two class variables:
        block_expiration_times (dict): key (str)- user ip,
                                       value (datetime) - end of blocking.
        candidates (dict): key (str) - user ip,
                           value (list) - list of datetime of at most
                           3 failed attempts to login.
    """

    def __init__(self, output_filename):
        """ Initialize attributes to keep track of users login attempts. """
        self.block_expiration_times = {}
        self.candidates = {}
        self.output_filename = output_filename  #

    def check_request(self, request):
        """
        Check user request and decide whether user already blocked, should be blocked,
        or added to a list of the candidates on block.
        """
        ip = request["ip"]

        if ip in self.block_expiration_times.keys():
            if request["date"] < self.block_expiration_times[ip]:
                # write blocked request to file
                self.write_blocked_request(request)
                return
            else:
                del self.block_expiration_times[ip]

        if request["url"] == "/login":
            # 3 cases
            # case 1: ip already in candidate list and HTTP code == 401
            # case 2: ip in candidate list and HTTP code != 401
            # case 3: ip is not in candidate list and HTTP code == 401
            if ip in self.candidates.keys():
                if request["response_code"] == "401":
                    self.update_candidate_list(request)
                else:
                    self.delete_from_candidate_list(request)
            else:
                if request["response_code"] == "401":
                    self.add_to_candidate_list(request)

    def write_blocked_request(self, request):
        """ Format information and write it to log file. """
        log = request["ip"] + " - - [" + \
            request["date"].strftime(date_formatting) + "] \"" + \
            request["request"] + "\" " + request["response_code"] + " " + \
            request["response_length"]
        write_information_to_file(self.output_filename, log)

    def update_candidate_list(self, request):
        """ Check if some failed request are expired, add new one. """
        failed_requests_dates = self.candidates[request["ip"]]
        for i in range(0, len(failed_requests_dates)):
            if (failed_requests_dates[i] - request["date"]).seconds < 20:
                failed_requests_dates.pop(i)
        failed_requests_dates.append(request["date"])
        if len(failed_requests_dates) == 3:
            self.block_user(request["ip"], request["date"])

    def delete_from_candidate_list(self, request):
        """ Delete request time from candidates. """
        del self.candidates[request["ip"]]

    def add_to_candidate_list(self, request):
        """ Add new ip to candidates. """
        self.candidates[request["ip"]] = [request["date"]]

    def block_user(self, ip, start_time):
        """
        Add user to banned list.
        Attributes:
            ip (str): user ip/host
            start_time (datetime): time of the last failed attempt to login
        """
        self.block_expiration_times[ip] = start_time + timedelta(0, 300)
