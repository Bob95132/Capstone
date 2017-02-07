import ConfigParser
import logging
import datetime
import os

CONFIG_FILENAME = 'RFManager/conf/rfid.conf'

# Gets the value for a given key 'keyname' from the properties file 'filepath'
def get_property(keyname, section):
    cp = ConfigParser.ConfigParser()
    cp.read(CONFIG_FILENAME)
    try:
        return cp.get(section, keyname)
    except ConfigParser.NoOptionError:
        logging.error( "Option %s not found in configuration file: %s Quitting..." % (keyname, CONFIG_FILENAME))

def read_status_file():
    filename = get_property("RF_STATUS_PATH", "CONFIGS") + get_property("RF_STATUS_FILE", "CONFIGS")
    fd = -1
    if os.path.exists(filename):
        try:
            fd = open(filename, 'r+')
        except (OSError, IOError) as e:
            logging.error( 'error reading RF_STATUS file.')
            return -1

    return fd

def report_status():
    fd = read_status_file()
    if fd is -1:
        return (0, 'Waiting to scan inventory')
    else:
        lines = fd.readlines()
        last_line = lines[len(lines) - 1]
        #check the first status flag
        if last_line[0] is '0':
            #inventory scan stopped
            if last_line[1] is '1':
                #there was an error
                return (3, 'Inventory scan terminated by error: %s' % last_line[2:])
            else:
                #inventory scan finished successfuly
                timestamp = last_line.split(' ')[1]
                return (2, 'Inventory scan finished successfuly at time: %s' % timestamp)
        else:
            #inventory scan is still running
            message = 'Inventory scan is running...\n'

            start_time = lines[0].split(' ')[1]
            message += 'started: %s\n' % start_time

            try:
                strt = datetime.datetime.strptime(start_time, '{%Y-%m-%d_%H.%M.%S}')
                difference = datetime.datetime.now() - strt
                minutes = difference.minute
                message += 'runtime: %d minutes', minutes
            except:
                logging.error( 'error calculating time difference')

            return (1, message)
