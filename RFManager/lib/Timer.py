# Timer - for keeping time
# Author: Mike G. Abood
# Capstone Fall 2016

import datetime

class Timer:
    def __init__(self):
        self.start_datetime = self.capture_start_time()
        self.end_datetime = None
        self.timestamp_start = self.timestamp_file(self.start_datetime)
        self.timestamp_end = None
        self.timestamp_start_pretty = self.timestamp_pretty(self.start_datetime)
        self.timestamp_end_pretty = None

    def capture_start_time(self):
        if self.start_datetime is None:
            return datetime.datetime.now()
        else:
            return self.start_datetime

    def timestamp_file(self, date):
        return '{:%Y-%m-%d_%H.%M.%S}'.format(date)

    def timestamp_pretty(self, date):
        return '{:%Y-%m-%d %H:%M:%S}'.format(date)

    def capture_stop_time(self):
        if self.end_datetime is None:
            self.end_datetime = datetime.datetime.now()
            self.timestamp_end = self.timestamp_file(self.end_datetime)
            self.timestamp_end_pretty = self.timestamp_pretty(self.end_datetime)
        else:
            return self.timestamp_end_pretty