# Utils - Utilities for RFManager
# Author: Mike G. Abood
# Capstone Fall 2016

import ConfigParser
import logging
import sys
import os

CONFIG_FILENAME = 'RFManager/rfid.conf'
LOG_FILE = 'RFManager/rfid.log'
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
def setup_logger(logfile, verbose, console):
    logging.getLogger('').handlers = []
    logging.basicConfig(level=logging.DEBUG,
                        format='RFID~[%(levelname)s] %(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d-%H:%M:%S',
                        filename=logfile,
                        filemode='a')
    if console:
        console = logging.StreamHandler()
        formatter = logging.Formatter('RFID~[%(levelname)s] %(asctime)s, %(message)s', '%Y-%m-%d-%H:%M:%S')
        console.setFormatter(formatter)
        if verbose:
            console.setLevel(logging.DEBUG)
        else:
            console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)

def report_dir_exists():
    return os.path.exists(get_property("RFSCAN_PATH", "CONFIGS"))

#checks for required files and fails out if not found
def check_files():
    if not os.path.exists(CONFIG_FILENAME):
        report_failed_and_exit('config file %s not found.' % CONFIG_FILENAME)

    scan_data_dir = get_property("RFSCAN_PATH", "CONFIGS")
    if not report_dir_exists():
        os.makedirs(scan_data_dir)

# Reports setup failure and exits the program with error status
def report_failed_and_exit(message=None):
    if message:
        logging.error('FAILED: %s' % message)

    logging.error("RF Manager EXITING")
    sys.exit(1)

#create pretty title in logs
def log_title(title):
    LINE_WIDTH = int(get_property("LINE_WIDTH", 'CONFIGS'))

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






