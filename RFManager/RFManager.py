#RFManager
from TagStore import *
from ReaderCom import *
import re
import time

def main():
    #Check files
    check_files()

    #Read configs
    POLLING_INTERVAL = float(get_property("POLLING_INTERVAL", "CONFIGS"))
    FWRITE_INTERVAL = float(get_property("FWRITE_INTERVAL", "CONFIGS"))
    VERBOSE_lOGS = int(get_property('VERBOSE', 'CONFIGS'))

    #setup logger
    setup_logger(LOG_FILE, VERBOSE_lOGS)
    log_title('RFID Manager')

    #initialize RFCom
    rcom = ReaderCom()
    logging.info('%s response: %s' % (rcom.rfcom_name, rcom.reader.response.strip('\n')))

    #rcom.setup_reader()
    rcom.config_reader()

    tstore = TagStore()
    fwrite_counter = 0

    try:
        while(True):
            rcom.poll_reader(tstore)

            time.sleep(POLLING_INTERVAL)
            fwrite_counter += POLLING_INTERVAL

            if fwrite_counter >= FWRITE_INTERVAL:
                logging.info('Writing Tags to File...')
                tstore.file_dump_json()
                tstore.file_dump_xls()
                fwrite_counter = 0

    except KeyboardInterrupt:
        logging.info('Exiting polling loop...')
        logging.info('Writing Tags to File...')
        tstore.file_dump_json()
        tstore.file_dump_xls()
        logging.info('\n' + tstore.get_contents_str())

        rcom.destroy_reader()
        rcom.rfcom_terminate()
        sys.exit(0)



if __name__ == '__main__':
    main()