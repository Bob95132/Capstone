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


class RFStatusCheck():
    def __init__(self):
        self.filename = get_property("RF_STATUS_PATH", "CONFIGS") + get_property("RF_STATUS_FILE", "CONFIGS")
        self.a_codes = {
            'STOPPED': get_property("STATUS_CODE_STOPPED", "CONFIGS"),
            'RUNNING': get_property("STATUS_CODE_RUNNING", "CONFIGS"),
            'FWRITE' : get_property("STATUS_CODE_FWRITE", "CONFIGS")
        }
        self.b_codes = {
            'SUCCESS': get_property("STATUS_CODE_SUCCESS", "CONFIGS"),
            'ERROR': get_property("STATUS_CODE_ERROR", "CONFIGS")
        }
        self.status_states = {
            0 : 'Checking Status...',
            1 : 'Waiting to scan inventory.',
            2 : 'Inventory scan in progress.',
            3 : 'Inventory scan completed successfully.',
            4 : 'Inventory scan failed.'
        }

    def read_status_file(self):
        fd = -1
        if os.path.exists(self.filename):
            try:
                fd = open(self.filename, 'r+')
            except (OSError, IOError) as e:
                logging.error( 'error reading RF_STATUS file.')
                return -1

        return fd

    def check_rf_state(self):
        fd = self.read_status_file()
        if fd is -1:
            state = 1
        else:
            lines = fd.readlines()
            last_line = lines[len(lines) - 1]

            # check the first status flag
            if last_line[0] is self.a_codes['STOPPED']:
                # inventory scan stopped
                if last_line[1] is self.b_codes['ERROR']:
                    # there was an error
                    state = 4
                else:
                    state = 3
            else:
                state = 2
            fd.close()

        return state

    def read_start_time(self):
        fd = self.read_status_file()
        time = '-'
        if fd > 0:
            lines = fd.readlines()
            if lines[0][0] is self.a_codes['RUNNING'] and lines[0][1] is self.b_codes['SUCCESS']:
                time = lines[0].split('|')[1]
            fd.close()
        return time

    def calculate_runtime(self):
        start = datetime.datetime.strptime(self.read_start_time(), '%m-%d-%Y %H:%M:%S')
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=(now-start).total_seconds())
        return (delta / 60, delta % 60)


    def has_written_file(self, extension):
        if extension[0] != '.':
            extension = '.' + extension
        fd = self.read_status_file()
        fw = False
        if fd > 0:
            lines = fd.readlines()
            for line in lines:
                if line[0] is self.a_codes['FWRITE']:
                    name = line.split('|')[2].strip()
                    if name[len(name) - len(extension):] is extension:
                        fw = True
            fd.close()
        return fw

    def read_file_name(self, extension):
        if extension[0] != '.':
            extension = '.' + extension
        fd = self.read_status_file()
        filename = None
        if fd > 0:
            lines = fd.readlines()
            for line in lines:
                if line[0] is self.a_codes['FWRITE']:
                    name = line.split('|')[2].strip()
                    if name[len(name) - len(extension):] is extension:
                        filename = name
            fd.close()
        return filename

    def get_scan_data_path(self):
        return get_property("ROOT_DIR", "CONFIGS") + get_property("RFSCAN_PATH", "CONFIGS")

    def read_tag_file(self, filename):
        try:
            fd = open(self.get_scan_data_path() + filename, 'r+')
            return fd.read()
        except:
            return None

    def read_error(self):
        fd = self.read_status_file()
        error = '-'
        if fd > 0:
            lines = fd.readlines()
            for line in lines:
                if line[0] is self.a_codes['STOPPED'] and line[1] is self.b_codes['ERROR']:
                    error = line[line.index('|') + 1:]
            fd.close()
        return error
