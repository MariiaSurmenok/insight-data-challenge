""" """

import sys
from collections import Counter
from datetime import timedelta

import failed_login

from io_utils import date_formatting, read_from_file, write_information_to_file


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


filename = sys.argv[1]
hosts_filename = sys.argv[2]
hours_filename = sys.argv[3]
resources_filename = sys.argv[4]
blocked_filename = sys.argv[5]

# filename = "../insight_testsuite/tests/test_features/log_input/log.txt"
# filename = "../log_input/log.txt"
ip_frequency = Counter()
resources = Counter()

# Calculate feature 1 and feature 2
print("Feature 1 and 2 start")

for entry in read_from_file(filename):
    count_host_frequency(ip_frequency, entry)
    count_bandwidth_resources(resources, entry)

top_hosts = ip_frequency.most_common(10)

# Write results to a file
for host in top_hosts:
    information = host[0] + "," + str(host[1])
    write_information_to_file(hosts_filename, information)

top_resources = resources.most_common(10)

# Write results to a file
for resource in top_resources:
    write_information_to_file(resources_filename, resource[0])

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
start = request["date"]
stop = start + timedelta(0, 3600)


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
    while request["date"] >= stop:
        # Save only the top 10 popular hours.
        date_stamp = start.strftime(date_formatting)
        save_hour(date_stamp, popular_dates, requests_per_hour)
        # Save statistics and shift time by 1 second
        requests_per_hour.pop(0)
        requests_per_hour.append(0)
        start = start + timedelta(0, 1)
        stop = stop + timedelta(0, 1)

    requests_per_hour[(request["date"] - start).seconds] += 1

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

# Write it in file
print(len(popular_dates.values()))
print(popular_dates)

# FEATURE 4
access_blocker = failed_login.AccessBlocker(blocked_filename)

for entry in read_from_file(filename):
    access_blocker.check_request(entry)