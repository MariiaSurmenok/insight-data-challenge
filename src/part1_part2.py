import re
from collections import Counter

def parse_log_line(log_line):
    """
    Parse log string into ip, date, request_method, url, protocol, response_code, and response_length
    Return result as a dictionary
    """
    pattern = '(?P<ip>\S+).*' + \
              '\[(?P<date>.+)\]\s*' + \
              '"(?P<request_method>\S+)\s+(?P<url>\S+)\s+(?P<protocol>\S+)"\s*' + \
              '(?P<response_code>\d+)\s+(?P<response_length>\d+|-)'

    regex = re.compile(pattern)
    result = regex.match(log_line)
    if result:
        return result.groupdict()


# count frequency of ip
# count bandwidth of resources
ip_frequency = Counter()
resources = Counter()
# filename = "../insight_testsuite/tests/test_features/log_input/log.txt"
filename = "../log_input/log.txt"
try:
    with open(filename) as f_obj:
        for line in f_obj:
            data = parse_log_line(line)

            if data:
                # Calculate hosts frequency (feature 1)
                ip_frequency[data["ip"]] += 1
                # Calculate bandwidth resources
                if data["response_length"].strip() != "-":
                    resources[data["url"]] += int(data["response_length"])
except FileNotFoundError:
    print("count_host_frequency: File not found")

print(ip_frequency.most_common(10))
print(resources.most_common(10))
