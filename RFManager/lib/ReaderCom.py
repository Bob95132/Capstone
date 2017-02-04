# ReaderCom - All Reader Interactions Communicating on ProcessPipe
# Author: Mike G. Abood
# Capstone Fall 2016

from Utils import *
from ProcessPipe import *
import re

class ReaderCom(object):
    def __init__(self, start_time):
        self.rfcom_path = get_property("RFCOM_PATH", "CONFIGS")
        self.rfcom_name = get_property("RFCOM_NAME", "CONFIGS")

        self.rfcom_timeout = float(get_property("TIMEOUT", "CONFIGS"))
        self.rfcom_err = get_property("RFCOM_ERROR_FLAG", "CONFIGS")
        self.rfcom_data_flag = get_property("RFCOM_DATA_RECV_FLAG", "CONFIGS")
        self.rfcom_data_term_flag = get_property("RFCOM_DATA_TERM_FLAG", "CONFIGS")

        self.cmd_rfdump = get_property("API_DUMPTAGS", "READER_PROPERTIES")
        self.device_name = get_property('DEVICE_NAME', 'READER_PROPERTIES')
        self.com_type = get_property('COM_TYPE', 'READER_PROPERTIES')
        self.reader = self.rfcom_init()

        self.status_dir = get_property("RF_STATUS_PATH", "CONFIGS")
        self.status_filename = get_property("RF_STATUS_FILE", "CONFIGS")
        self.write_status_file(start_time, init=True)

    # Create, or append a line to the RF_STATUS file
    def write_status_file(self, append_str=None, append_lst=None, init=False):
        try:
            if init:
                fd = open(self.status_dir + self.status_filename, 'a+')
            else:
                fd = open(self.status_dir + self.status_filename, 'w')

            if append_str:
                fd.write(append_str)

            if append_lst:
                fd.writelines(append_lst)

            fd.close()

        except (OSError, IOError) as e:
            logging.error('error writing RF_STATUS file.')

    # Initialize ProcessPipe object
    def rfcom_init(self):
        logging.info('starting %s...' % self.rfcom_name)
        return ProcessPipe(self.rfcom_path + self.rfcom_name, timeout=self.rfcom_timeout)

    # method to send -c command to reader using expect on response
    def reader_communicate(self, cmd, fail_flag, success_flag, opt_flag=None):
        arg_string = '-c %s' % cmd
        logging.debug('executing command: %s' % arg_string)
        err = 0

        self.reader.sendline(arg_string)
        index = self.reader.expect(self.rfcom_err, fail_flag, success_flag, opt_flag)
        if index < 0:  # TIMEOUT reached
            logging. error('Reader timed out or sent EOF. Response: %s' % self.reader.response)
            report_failed_and_exit('child process timed out.')

        if index == 0 or index == 1:  # ERROR matched on output
            err = 1
            logging.error('Reader command: %s Failed.' % cmd)

        return (err, self.reader.response)

    # run setup command on reader
    def setup_reader(self):
        logging.info('setting up RFCom connection for %s using com_type %s' %
                     (self.device_name, self.com_type))
        arg_string = '-s %s %s' % (self.device_name, self.com_type)
        logging.debug('sending command: %s' % arg_string)

        self.reader.sendline(arg_string)
        index = self.reader.expect('CONNECTION_FAILURE', 'CONNECTION_SUCCESS')
        if index <= 0:
            logging.error('RFCom output: %s' % self.reader.response)
            report_failed_and_exit('RFCom setup failed.')

        logging.info('RFCom response: %s' % self.reader.response.strip('\n'))

    # run sequence of config commands from rfid.conf
    def config_reader(self):
        logging.info('running reader configuration commands...')
        config_seq = get_property('CONFIG_SEQUENCE', 'READER_CONFIGS')
        sequence = config_seq.split('|')

        for step in sequence:
            output = self.reader_communicate(step, 'ERROR', 'CMD_SUCCESS', opt_flag='RECEIVED_DATA:.*')
            if output[0] == 0:
                logging.info('RFCom response: %s' % output[1].strip('\n'))
            else:
                logging.error('RFCom response: %s' % output[1].strip('\n'))
                report_failed_and_exit('reader configuration failed at command: %s' % step)

    # send polling command to reader, process data returned
    def poll_reader(self, tstore):
        logging.info('polling RF reader...')
        output = self.reader_communicate(self.cmd_rfdump, 'ERROR', 'END')
        if output[0] == 0:
            logging.info('RFCom response: \n%s' % output[1].strip('\n'))

            data = self.extract_data(output[1])
            tags = self.clean_data(data)
            tstore.add_tags(tags)
        else:
            logging.error('RFCom Polling ERROR')
            logging.error('RFCom response: %s' % output[1].strip('\n'))

    # Tear down connection with reader
    def destroy_reader(self):
        logging.info('Destroying reader...')

        arg_string = '-d'
        logging.debug('sending command: %s' % arg_string)
        self.reader.sendline(arg_string)
        index = self.reader.expect(self.rfcom_err, 'CLOSE_FAILURE', 'CLOSE_SUCCESS')

        if index <= 1:
            logging.error('RFCom destroy ERROR')
            logging.error('RFCom response: %s' % self.reader.response)

        else:
            logging.info('Reader destroyed.')
            logging.info('RFCom response: %s' % self.reader.response.strip('\n'))

    # Terminate child process
    def rfcom_terminate(self):
        logging.info('Terminating RFCom...')

        arg_string = '-q'
        logging.debug('sending command: %s' % arg_string)

        self.reader.sendline(arg_string)
        index = self.reader.expect(self.rfcom_err, 'EXITING')

        if index <= 0:
            logging.error('Error terminating RFCom')
            logging.error('RFCom response: %s' % self.reader.response.strip('\n'))
        else:
            logging.info('Process Terminated.')

    # Extract tag data from reader output
    def extract_data(self, data):
        # 'some garbage data RECEIVED_DATA: tag1, tag2, tag3, END'
        start = data.index(self.rfcom_data_flag) + len(self.rfcom_data_flag)
        end = data.index(self.rfcom_data_term_flag)
        return data[start:end].strip()

    # remove unwanted strings from tag data
    def clean_data(self, data):
        tags = filter(None, re.split('[\n\r]', re.sub('RECEIVED_DATA:', '', data)))
        tags = filter(lambda x: ',' in x, tags)
        tags = map(lambda x: re.split('[,]', x), tags)
        ids = []
        for line in tags:
            for field in line:
                if field.isdigit():
                    ids.append(field)
                    break
        return ids


