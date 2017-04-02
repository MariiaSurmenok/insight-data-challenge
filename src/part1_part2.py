import re
from collections import Counter


def parse_log_line(log_line):
    """
    Parse log string into ip, date, request_method, url, protocol, response_code, and response_length.
    Return result as a dictionary.
    """
    pattern = '(?P<ip>\S+).*' + \
              '\[(?P<date>.+)\]\s*' + \
              '"(?P<request_method>\S+)\s+(?P<url>\S+)\s+(?P<protocol>\S+)"\s*' + \
              '(?P<response_code>\d+)\s+(?P<response_length>\d+|-)'

    regex = re.compile(pattern)
    result = regex.match(log_line)
    if result:
        return result.groupdict()


def read_from_file(file):
    """
    Generator that reads line by line from log file.
    """
    try:
        with open(file) as f_obj:
            for line in f_obj:
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
#filename = "../log_input/log.txt"
ip_frequency = Counter()
resources = Counter()

for entry in read_from_file(filename):
    count_host_frequency(ip_frequency, entry)
    count_bandwidth_resources(resources, entry)

top_hosts = ip_frequency.most_common(10)
top_resources = resources.most_common(10)

for host in top_hosts:
    information = host[0] + "," + str(host[1])
    write_information_to_file("../log_output/hosts.txt", information)

for resource in top_resources:
    write_information_to_file("../log_output/resources.txt", resource[0])
