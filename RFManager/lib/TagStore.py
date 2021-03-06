# TagStore - Object for Storing RFID Tags
# Author: Mike G. Abood
# Capstone Fall 2016

import RFStatus
import collections
import datetime
from utils import get_property
import json
import xlsxwriter

class TagStore:
    def __init__(self, start_timestamp):
        self.size = 0
        self.tag_map = collections.defaultdict()
        self.dirpath = get_property("RFSCAN_PATH", "CONFIGS")
        self.filename = get_property("RFSCAN_FILE", "CONFIGS")
        self.file_time = start_timestamp
        self.start_time = self.timestamp_pretty()

    def add_tags(self, ids):
        for id in ids:
            self.tag_map[id] = self.timestamp_pretty()

        self.size = len(self.tag_map)

    def file_dump_json(self):
        dr = self.dirpath
        fn = self.filename + self.file_time
        fn += '.json'

        json_data = {
            'RF Tags Identified': {
                'metadata':{
                    'collection_start_time': self.start_time,
                    'collection_stop_time': self.timestamp_pretty()
                },
                'data':self.tag_map
            }
        }
        with open(dr + fn, 'w+') as outfile:
            outfile.write(json.dumps(json_data, indent=4, sort_keys=True))
            outfile.close()

        RFStatus.RFStatus().file_write('Tags written to JSON file', fn)

    def file_dump_xls(self):
        dr = self.dirpath
        fn = self.filename + self.file_time
        fn += '.xlsx'

        title = 'RFID Tag Collection Report'

        row = 0
        col = 0

        workbook = xlsxwriter.Workbook(dr + fn)
        worksheet = workbook.add_worksheet()

        worksheet.set_column(0, 0, len(title))
        worksheet.write(row, col, title)
        row += 1
        worksheet.write(row, col, 'Collection start time')
        worksheet.set_column(1, 1, len(self.start_time))
        worksheet.write(row, col + 1, self.start_time)
        row += 1
        worksheet.write(row, col, 'Collection stop time')
        worksheet.write(row, col + 1, self.timestamp_pretty())
        worksheet.set_column(2, 2, 6)
        row = 0
        col = 3

        #worksheet formatting
        worksheet.set_column(3, 3, 10)
        worksheet.write(row, col, 'Tag ID')
        worksheet.set_column(4, 4, len(self.timestamp_pretty()))
        worksheet.write(row, col + 1, 'Time Identified')
        row += 1

        for key in self.tag_map:
            worksheet.write(row, col, key)
            worksheet.write(row, col + 1, self.tag_map[key])
            row += 1

        workbook.close()

        RFStatus.RFStatus().file_write('Tags written to XLSX file', fn)

    def get_contents_str(self):
        contents = 'TagStore: {'
        for key in self.tag_map:
            contents += '\n\t' + '%s : %s,' % (str(key), str(self.tag_map[key]))
        contents = contents[:-1]
        contents += '\n}\n'
        return contents

    def timestamp_pretty(self):
        return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
