""" """

import sys
from collections import Counter
from datetime import timedelta

import failed_login
import busiest_hours

from io_utils import date_formatting, read_from_file, write_information_to_file


# File paths
filename = sys.argv[1]
hosts_filename = sys.argv[2]
hours_filename = sys.argv[3]
resources_filename = sys.argv[4]
blocked_filename = sys.argv[5]

# filename = "../insight_testsuite/tests/test_features/log_input/log.txt"
# filename = "../log_input/log.txt"


# Feature 1 implementation
def count_host_frequency(counter, data):
    """
    Feature 1 implementation:
    Counts how many times hosts/IP addresses have accessed the site.
    Attributes:
        counter (Counter class): keeps track of all hosts
        data (dict): parsed information about request
    """
    if data:
        counter[data["ip"]] += 1


# Feature 2 implementation
def count_bandwidth_resources(counter, data):
    """
    Feature 2 implementation:
    Counts how many bytes were sent for particular resources.
    Attributes:
        counter (Counter class): keeps overall bytes for particular resource
        data (dict): parsed information about request
    """
    if data:
        if data["response_length"].strip() != "-":
            counter[data["url"]] += int(data["response_length"])


# Calculate feature 1 and feature 2
print("Feature 1 and 2 start")

ip_frequency = Counter()
resources = Counter()

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
print("Feature 3 starts")
load_meter = busiest_hours.LoadMeter(filename, hours_filename)
load_meter.find_busiest_hours()


print("Feature 3 stops")

# FEATURE 4
access_blocker = failed_login.AccessBlocker(blocked_filename)

for entry in read_from_file(filename):
    access_blocker.check_request(entry)
