#RFManager
from Utils import *
from TagStore import *
from ProcessPipe import *
import re
import time

RFCOM_PATH = get_property("RFCOM_PATH", "CONFIGS")
RFCOM_NAME = get_property("RFCOM_NAME", "CONFIGS")
CMD_RFDUMP = get_property("API_DUMPTAGS", "READER_PROPERTIES")
POLLING_INTERVAL = float(get_property("POLLING_INTERVAL", "CONFIGS"))
FWRITE_INTERVAL = float(get_property("FWRITE_INTERVAL", "CONFIGS"))

#run setup command on reader
def setup_reader(process):
    device_name = get_property('DEVICE_NAME', 'READER_PROPERTIES')
    com_type = get_property('COM_TYPE', 'READER_PROPERTIES')

    logging.info('setting up RFCom connection for %s using com_type %s' % (device_name, com_type))
    arg_string = '-s %s %s' % (device_name, com_type)
    logging.debug('sending command: %s' % arg_string)

    process.sendline(arg_string)
    index = process.expect('Failed', 'Success')
    if index <= 0:
        logging.error('RFCom output: %s' % process.response)
        report_failed_and_exit('RFCom setup failed.')

    logging.info('RFCom response: %s' % process.response.strip('\n'))

#method to send -c command to reader using expect on response
def reader_communicate(process, cmd):
    arg_string = '-c %s' % cmd
    logging.debug('executing command: %s' % arg_string)
    err = 0

    process.sendline(arg_string)
    index = process.expect('ERROR', 'RECEIVED_DATA:.*')

    if index < 0: #TIMEOUT reached
        logging.error('Reader sent unexpected response: ' % process.response)
        report_failed_and_exit('child process timed out.')

    if index == 0: #ERROR matched on output
        err = 1
        logging.error('Reader command: %s Failed.' % cmd)

    return (err, process.response)

#run sequence of config commands from rfid.conf
def config_reader(process):
    logging.info('running reader configuration commands...')
    config_seq = get_property('CONFIG_SEQUENCE', 'READER_CONFIGS')
    sequence = config_seq.split('|')

    for step in sequence:
        output = reader_communicate(process, step)
        if output[0] == 0:
            logging.info('RFCom response: %s' % output[1].strip('\n'))
        else:
            logging.error('RFCom response: %s' % output[1].strip('\n'))
            report_failed_and_exit('reader configuration failed at command: %s' % step)

#send polling command to reader, process data returned
def poll_reader(process, tstore):
    logging.info('polling RF reader...')
    output = reader_communicate(process, CMD_RFDUMP)
    if output[0] == 0:
        logging.info('RFCom response: %s' % output[1].strip('\n'))
        #parse reader data for list of tags
        tags = filter(None, re.split('[ \n\r]', re.sub('RECEIVED_DATA:', '', output[1])))
        #add these tags to TagStore object
        tstore.add_tags(tags)
    else:
        logging.error('RFCom Polling ERROR')
        logging.error('RFCom response: %s' % output[1].strip('\n'))



def main():
    setup_logger(LOG_FILE, int(get_property('VERBOSE', 'CONFIGS')))
    log_title('RFID Manager')

    logging.info('starting %s...' % RFCOM_NAME)
    rfcom = ProcessPipe(RFCOM_PATH + RFCOM_NAME, timeout=2.5)
    logging.info('%s response: %s' % (RFCOM_NAME, rfcom.response.strip('\n')))

    #setup_reader(rfcom)
    config_reader(rfcom)

    tstore = TagStore()
    fwrite_counter = 0

    try:
        while(True):
            poll_reader(rfcom, tstore)

            time.sleep(POLLING_INTERVAL)
            fwrite_counter += POLLING_INTERVAL

            if fwrite_counter >= FWRITE_INTERVAL:
                tstore.file_dump()

    except KeyboardInterrupt:
        logging.info('Exiting polling loop...')
        logging.info('Writing TagStore to File...')
        tstore.file_dump()
        logging.info('\n' + tstore.get_contents_str())
        sys.exit(0)



if __name__ == '__main__':
    main()