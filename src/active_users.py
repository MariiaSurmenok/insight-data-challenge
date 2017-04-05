"""
Implementation of feature 1:
Find active hosts/IP addresses that have accessed the site.
"""


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
