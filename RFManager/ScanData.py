import json
from os import listdir
from os.path import isfile, join
from Utils import *

RFSCAN_PATH = get_property("RFSCAN_PATH", "CONFIGS")
RFSCAN_FILE = get_property("RFSCAN_FILE", "CONFIGS")

def main():
    if report_dir_exists():
        try:
            dir = [f for f in listdir(RFSCAN_PATH) if isfile(join(RFSCAN_PATH, f))]
            print 'ScanDir: ' + str(dir)

            file = sorted(filter(lambda x: '.json' in x, dir), reverse=True)[0]

            print file
            fd = open(RFSCAN_PATH + '/' + file, 'r+')
            obj = json.load(fd)['RF Tags Identified']
            if 'data' in obj:
                print '%d Tags Identified' % len(obj['data'])
                print json.dumps(obj, indent=4, sort_keys=True)
            else:
                print 'No Tags Identified'

        except:
            print 'Output file not found'
    else:
        print 'ScanData dir not found'


if __name__ == '__main__':
    main()