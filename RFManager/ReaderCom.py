# ReaderCom - All Reader Interactions Communicating on ProcessPipe
# Author: Mike G. Abood
# Capstone Fall 2016

from Utils import *
from ProcessPipe import *
import re

class ReaderCom(object):
    def __init__(self):
        self.rfcom_path = get_property("RFCOM_PATH", "CONFIGS")
        self.rfcom_name = get_property("RFCOM_NAME", "CONFIGS")
        self.rfcom_timeout = float(get_property("TIMEOUT", "CONFIGS"))
        self.rfcom_err = get_property("RFCOM_ERROR_FLAG", "CONFIGS")
        self.cmd_rfdump = get_property("API_DUMPTAGS", "READER_PROPERTIES")
        self.device_name = get_property('DEVICE_NAME', 'READER_PROPERTIES')
        self.com_type = get_property('COM_TYPE', 'READER_PROPERTIES')
        self.reader = self.rfcom_init()

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
            logging.error('Reader sent unexpected response: %s' % self.reader.response)
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
            output = self.reader_communicate(step, 'ERROR', 'RECEIVED_DATA:.*', 'CMD_SUCCESS')
            if output[0] == 0:
                logging.info('RFCom response: %s' % output[1].strip('\n'))
            else:
                logging.error('RFCom response: %s' % output[1].strip('\n'))
                report_failed_and_exit('reader configuration failed at command: %s' % step)

    # send polling command to reader, process data returned
    def poll_reader(self, tstore):
        logging.info('polling RF reader...')
        output = self.reader_communicate(self.cmd_rfdump, 'ERROR', 'RECEIVED_DATA:.*')
        if output[0] == 0:
            logging.info('RFCom response: %s' % output[1].strip('\n'))
            # parse reader data for list of tags
            tags = filter(None, re.split('[\n\r]', re.sub('RECEIVED_DATA:', '', output[1])))
            ids = map(lambda x: re.split('[,]', x)[1].strip(' '), filter(lambda x: ',' in x,tags))
            # add these tags to TagStore object
            tstore.add_tags(ids)
        else:
            logging.error('RFCom Polling ERROR')
            logging.error('RFCom response: %s' % output[1].strip('\n'))

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

