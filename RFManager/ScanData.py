import json
from os import listdir
from os.path import isfile, join
from Utils import *

RFSCAN_PATH = get_property("RFSCAN_PATH", "CONFIGS")
RFSCAN_FILE = get_property("RFSCAN_FILE", "CONFIGS")

def main():
    if report_dir_exists():
        dir = [f for f in listdir(RFSCAN_PATH) if isfile(join(RFSCAN_PATH, f))]
        file = sorted(filter(lambda x: '.json' in x, dir), reverse=True)[0]
        try:
            fd = open(file, 'r')
            obj = json.load(fd)
            print '%d Tags Identified' % len(obj['data'])
            print json.dumps(object)

        except:
            print 'There was an error.'

    else:
        print 'ScanData dir not found'


if __name__ == '__main__':
    main()