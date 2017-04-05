"""
Implementation of feature 2:
Identify most popular resources on the site that consume the most bandwidth.
"""


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
