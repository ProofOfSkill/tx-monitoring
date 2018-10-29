import csv
import time
from pathlib import Path
from datetime import date


class Data:
    def __init__(self):
        self.path = '../data'
        self.headers = ['Timestamp', 'Number of TXID']
        self.initialize()

    # Initialize CSV file
    def initialize(self):
        file = "%s/%s_%s.csv" % (self.path, 'mempool', date.today())
        if not Path(file).is_file():
            # TODO check errors
            with open(file, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.headers, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()

    # Store mempool data in CSV file
    def write(self, data):
        file = "%s/%s_%s.csv" % (self.path, 'mempool', date.today())
        # TODO check errors
        with open(file, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow({'Timestamp': int(time.time()), 'Number of TXID': data['size']})

