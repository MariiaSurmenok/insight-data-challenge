""" Main file. All 4 features are running here. """

import sys
from collections import Counter
from datetime import timedelta

import active_users
import busiest_hours
import failed_login
import popular_resources

from io_utils import date_formatting, read_from_file, write_information_to_file


# File paths
filename = sys.argv[1]
hosts_filename = sys.argv[2]
hours_filename = sys.argv[3]
resources_filename = sys.argv[4]
blocked_filename = sys.argv[5]


# FEATURES 1 and 2
ip_frequency = Counter()
resources = Counter()

for entry in read_from_file(filename):
    active_users.count_host_frequency(ip_frequency, entry)
    popular_resources.count_bandwidth_resources(resources, entry)

top_hosts = ip_frequency.most_common(10)

# Write results to a file
for host in top_hosts:
    information = host[0] + "," + str(host[1])
    write_information_to_file(hosts_filename, information)

top_resources = resources.most_common(10)

# Write results to a file
for resource in top_resources:
    write_information_to_file(resources_filename, resource[0])


# FEATURE 3
load_meter = busiest_hours.LoadMeter(filename, hours_filename)
load_meter.find_busiest_hours()


# FEATURE 4
access_blocker = failed_login.AccessBlocker(blocked_filename)

for entry in read_from_file(filename):
    access_blocker.check_request(entry)
