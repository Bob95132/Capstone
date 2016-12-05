#Utils for RFID Manager

import ConfigParser
import logging
import sys

CONFIG_FILENAME = 'rfid.conf'
LOG_FILE = 'rfid.log'
EXIT_SUCCESS = 0

# Gets the value for a given key 'keyname' from the properties file 'filepath'
def get_property(keyname, section):
    cp = ConfigParser.ConfigParser()
    cp.read(CONFIG_FILENAME)
    try:
        return cp.get(section, keyname)
    except ConfigParser.NoOptionError:
        logging.error("Option %s not found in configuration file: %s Quitting..." % (keyname, CONFIG_FILENAME))
        sys.exit(1)

# Sets up logger with the configured log file
def setup_logger(logfile, verbose):
    logging.getLogger('').handlers = []
    logging.basicConfig(level=logging.DEBUG,
                        format='RFID~[%(levelname)s] %(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d-%H:%M:%S',
                        filename=logfile,
                        filemode='a')
    console = logging.StreamHandler()
    formatter = logging.Formatter('RFID~[%(levelname)s] %(asctime)s, %(message)s', '%Y-%m-%d-%H:%M:%S')
    console.setFormatter(formatter)
    if verbose:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

# Reports setup failure and exits the program with error status
def report_failed_and_exit(message=None):
    if message:
        logging.error('FAILED: %s' % message)

    logging.error("RF Manager EXITING")
    sys.exit(1)


def log_title(title):
    border_len = (LINE_WIDTH - len(title) - 4) / 2
    border = '|'
    for i in range(border_len):
        border += '-'
    border += ' ' + title + ' '
    if len(title) % 2 != 0:
        border += '-'
    for i in range(border_len):
        border += '-'
    border += '|'
    logging.info(border)

#load all constants
LINE_WIDTH = int(get_property("LINE_WIDTH", 'CONFIGS'))



