import re
from collections import Counter
from datetime import datetime
from datetime import timedelta


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
    request_pattern = '(?P<ip>\S+).*\s\[(?P<date>.+)\]\s*\"(?P<request>.+)\"\s*(?P<response_code>\d+)\s(?P<response_length>\d+|-)'
    url_pattern = '((GET|HEAD|POST)\s+)?(?P<request_url>.+?)\s+(HTTP.*)?$'
    request_regex = re.compile(request_pattern)
    url_regex = re.compile(url_pattern)

    parsed_request = request_regex.match(log_line)

    if parsed_request:
        result = parsed_request.groupdict()
        result["url"] = result["request"]
        parsed_url = url_regex.match(result["request"])
        if parsed_url:
            result["url"] = parsed_url.groupdict()["request_url"]
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


def count_host_frequency(counter, data):
    """
    Counts how many times hosts/IP addresses have accessed the site.
    Attributes:
        counter (Counter class): keeps track of all hosts
        data (dict): parsed information about request
    """
    if data:
        counter[data["ip"]] += 1


def count_bandwidth_resources(counter, data):
    """
    Counts how many bytes were sent for particular resources.
    Attributes:
        counter (Counter class): keeps overall bytes for particular resource
        data (dict): parsed information about request
    """
    if data:
        if data["response_length"].strip() != "-":
            counter[data["url"]] += int(data["response_length"])


def write_information_to_file(file, log_line):
    """
    Append information to a log file.
    Attributes:
        file (str): log file url
        log_line (str): information to append
    """
    with open(file, 'a') as f_obj:
        f_obj.write(log_line + "\n")


filename = "../insight_testsuite/tests/test_features/log_input/log.txt"
# filename = "../log_input/log.txt"
ip_frequency = Counter()
resources = Counter()

# Calculate feature 1 and feature 2
print("Feature 1 and 2 start")

for entry in read_from_file(filename):
    count_host_frequency(ip_frequency, entry)
    count_bandwidth_resources(resources, entry)

top_hosts = ip_frequency.most_common(10)
top_resources = resources.most_common(10)

# Write results to files
for host in top_hosts:
    information = host[0] + "," + str(host[1])
    write_information_to_file("../log_output/hosts.txt", information)

for resource in top_resources:
    write_information_to_file("../log_output/resources.txt", resource[0])

print("Feature 1 and 2 stop")
# FEATURE 3
# Need refactor
# Create array with size 3600 that will represent seconds in 60 minutes
# and save requests for each second

print("Feature 3 starts")

requests_per_hour = [0] * 3600
popular_dates = {}

generator = read_from_file(filename)
request = next(generator)
start = datetime.strptime(request["date"], '%d/%b/%Y:%H:%M:%S %z')
stop = start + timedelta(0, 3600)
date_formatting = '%d/%b/%Y:%H:%M:%S %z'


def save_hour(key_date, top_10, requests_in_current_hour):
    """
    Save number of requests in current hour
    if it is on of the 10 busiest hours

    Attributes:
        key_date (str): time when current hour started
        top_10 (dict): 10 most busiest hours
        requests_in_current_hour (list): list of requests in this hour
    """
    if len(top_10) == 10:
        if sum(requests_in_current_hour) > min(top_10.values()):
            del top_10[min(top_10, key=top_10.get)]
            top_10[key_date] = sum(requests_in_current_hour)
    else:
        top_10[key_date] = sum(requests_in_current_hour)


def update_statistics(start_date, stop_date, top_10, requests_in_current_hour):
    """
    Update statistics about top 10 busiest hours and shift time by 1 second
    Attributes:

    """
    # Save only the top 10 popular hours.


while request:
    request_date = datetime.strptime(request["date"], date_formatting)

    if request_date < stop:
        requests_per_hour[(request_date - start).seconds] += 1

    while request_date > stop:
        # Save only the top 10 popular hours.
        date_stamp = start.strftime(date_formatting)
        save_hour(date_stamp, popular_dates, requests_per_hour)
        # Save statistics and shift time by 1 second
        requests_per_hour.pop(0)
        requests_per_hour.append(0)
        start = start + timedelta(0, 1)
        stop = stop + timedelta(0, 1)
    try:
        request = next(generator)
    except StopIteration:
        request = None
        for i in range(0, 3600):
            # Count requests one more hour after the last request
            date_stamp = start.strftime(date_formatting)
            save_hour(date_stamp, popular_dates, requests_per_hour)
            # Shift by 1 second
            requests_per_hour.pop(0)
            requests_per_hour.append(0)
            start = start + timedelta(0, 1)


print(len(popular_dates.values()))
print(popular_dates)
