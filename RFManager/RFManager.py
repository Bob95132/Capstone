# RFManager - An interface RFID Reader Device
# Author: Mike G. Abood
# Capstone Fall 2016

from TagStore import *
from ReaderCom import *
import signal
import time

sig_flag = 0

def finish_and_dump(rcom, tstore, dump=1):
    logging.info('Exiting polling loop...')
    if dump:
        logging.info('Writing Tags to File...')
        tstore.file_dump_json()
        tstore.file_dump_xls()
        logging.info('\n' + tstore.get_contents_str())

    rcom.destroy_reader()
    rcom.rfcom_terminate()

    logging.info('RF Manager EXITING')
    sys.exit(0)

def handle_signal(signum, stack):
    sig_flag = 1

def main():
    #Check files
    check_files()

    #Read configs
    POLLING_INTERVAL = float(get_property("POLLING_INTERVAL", "CONFIGS"))
    FWRITE_INTERVAL = float(get_property("FWRITE_INTERVAL", "CONFIGS"))
    VERBOSE_lOGS = int(get_property('VERBOSE', 'CONFIGS'))
    CONSOLE_LOGS = int(get_property('CONSOLE', 'CONFIGS'))

    #setup logger
    setup_logger(LOG_FILE, VERBOSE_lOGS, CONSOLE_LOGS)
    log_title('RFID Manager')

    #initialize RFCom
    rcom = ReaderCom()
    logging.info('%s response: %s' % (rcom.rfcom_name, rcom.reader.response.strip('\n')))

    rcom.setup_reader()
    rcom.config_reader()

    tstore = TagStore()
    fwrite_counter = 0

    signal.signal(signal.SIGHUP, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while report_dir_exists() and not sig_flag:
            rcom.poll_reader(tstore)

            time.sleep(POLLING_INTERVAL)
            fwrite_counter += POLLING_INTERVAL

            if fwrite_counter >= FWRITE_INTERVAL:
                logging.info('Writing Tags to File...')
                tstore.file_dump_json()
                tstore.file_dump_xls()
                fwrite_counter = 0
        else:
            logging.error('Report directory removed.')
            finish_and_dump(rcom, tstore, sig_flag)

    except KeyboardInterrupt:
        finish_and_dump(rcom, tstore)



if __name__ == '__main__':
    main()