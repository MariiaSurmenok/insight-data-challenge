"""
Implementation of feature 3:
List in descending order the site’s 10 busiest
(i.e. most frequently visited) 60-minute period.
"""

from datetime import timedelta

from io_utils import date_formatting, read_from_file, write_information_to_file


class LoadMeter():
    """
    Calculates load for each hour with 1 second shift.

    Class variables:
        input_filename (str): url of log file.
        output_filename (str): url to write the result.
        requests_per_hour (list): represents seconds in 60 minutes.
        popular_dates (dict): keep top 10 busiest hours; key - date,
                              value - number of loads for this hour.
        start (datetime): the beginning of current hour.
        stop (datetime): the end of current hour.
    """

    def __init__(self, input_filename, output_filename):
        """
        Initialize class variables.
        Attributes:
            input_filename (str): url of log file.
            output_filename (str): destination to write result.
        """
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.requests_per_hour = [0] * 3600
        self.popular_dates = {}
        self.start = ""
        self.stop = ""

    def find_busiest_hours(self):
        generator = read_from_file(self.input_filename)
        request = next(generator)
        self.start = request["date"]
        self.stop = self.start + timedelta(0, 3600)

        while request:
            while request["date"] >= self.stop:
                self.update_statistics()

            self.requests_per_hour[(request["date"] - self.start).seconds] += 1

            try:
                request = next(generator)
            except StopIteration:
                request = None
                for i in range(0, 3600):
                    self.update_statistics()
        self.write_busiest_hours()

    def update_statistics(self):
        """
        Update statistics about top 10 busiest hours and shift time
        by 1 second.
        """
        # Save only the top 10 popular hours.
        date_stamp = self.start.strftime(date_formatting)
        self.save_hour(date_stamp)
        # Save statistics and shift time by 1 second
        self.requests_per_hour.pop(0)
        self.requests_per_hour.append(0)
        self.start = self.start + timedelta(0, 1)
        self.stop = self.stop + timedelta(0, 1)

    def save_hour(self, date_stamp):
        """
        Save number of requests in current hour
        if it is on of the 10 busiest hours.
        Attributes:
            date_stamp (str): formatted date of the beginning of current date.
        """
        if len(self.popular_dates) == 10:
            if sum(self.requests_per_hour) > min(self.popular_dates.values()):
                del self.popular_dates[
                    min(self.popular_dates, key=self.popular_dates.get)
                ]
                self.popular_dates[date_stamp] = sum(self.requests_per_hour)
        else:
            self.popular_dates[date_stamp] = sum(self.requests_per_hour)

    def write_busiest_hours(self):
        """ Format information and write it to output file. """
        top_10_hours = sorted(
            self.popular_dates.items(), key=lambda x: x[1], reverse=True
        )
        for entry in top_10_hours:
            log = entry[0] + "," + str(entry[1])
            write_information_to_file(self.output_filename, log)
