"""
Set of helper functions for reading, writing and parsing information
"""

import re
from datetime import datetime

date_formatting = '%d/%b/%Y:%H:%M:%S %z'
request_pattern = '(?P<ip>\S+).*\s\[(?P<date>.+)\]\s*\"(?P<request>.+)\"\s*(?P<response_code>\d+)\s(?P<response_length>\d+|-)'
url_pattern = '((GET|HEAD|POST)\s+)?(?P<request_url>.+?)\s+(HTTP.*)?$'


def parse_log_line(log_line):
    """
    Parse log string into ip, date, url,
    protocol, response_code, and response_length.
    Return parsed information as a dictionary.
    Attributes:
        log_line (str): one request from log file
    Return:
        dictionary with following keys:
            - ip
            - date
            - url
            - response_code
            - response_length
    """

    request_regex = re.compile(request_pattern)
    url_regex = re.compile(url_pattern)

    parsed_request = request_regex.match(log_line)

    if parsed_request:
        result = parsed_request.groupdict()
        result["url"] = result["request"]
        result["date"] = datetime.strptime(result["date"], date_formatting)
        parsed_url = url_regex.match(result["request"])
        if parsed_url:
            result["url"] = parsed_url.groupdict()["request_url"].strip()
        return result
    else:
        write_information_to_file("../log_output/corrupted_data.txt", log_line)


def read_from_file(file):
    """
    Generator that yields line from log file.
    Attributes:
        file (str): url to log file
    """
    try:
        with open(file) as f_obj:
            for line in f_obj:
                parsed_line = parse_log_line(line)
                if parsed_line:
                    yield parse_log_line(line)
    except FileNotFoundError:
        print("read_from_file: File not found")


def write_information_to_file(file, log_line):
    """
    Append information to a log file.
    Attributes:
        file (str): log file url
        log_line (str): information to append
    """
    with open(file, 'a') as f_obj:
        f_obj.write(log_line + "\n")