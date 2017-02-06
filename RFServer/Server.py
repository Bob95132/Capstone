from piui import PiUi
import RFStatusCheck
import os
import subprocess
import time
import logging

ui = PiUi()
page = ui.new_ui_page(title="RFConnect")
log_file = 'RFServer/logs/rfserver.log'

current_dir = os.path.dirname(os.path.abspath(__file__))

# Sets up logger with the configured log file
def setup_logger(logfile, verbose, console):
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.getLogger('').handlers = []
    logging.basicConfig(level=log_level,
                        format='RFSERV~[%(levelname)s] %(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d-%H:%M:%S',
                        filename=logfile,
                        filemode='w+')
    if console:
        console = logging.StreamHandler()
        formatter = logging.Formatter('RFSERV~[%(levelname)s] %(asctime)s, %(message)s', '%Y-%m-%d-%H:%M:%S')
        console.setFormatter(formatter)
        console.setLevel(log_level)
        logging.getLogger('').addHandler(console)

class RFServerUI(object):

    def __init__(self):
        self.title = None
        self.txt = None
        self.img = None
        self.ui = PiUi()
        self.src = None
        self.code_color = {
            0 : 'grey',
            1 : 'green',
            2 : 'blue',
            3 : 'red'
        }

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="RFConnect")
        self.title = self.page.add_textbox("RFID Inventory Scan", "h1")
        space = self.page.add_textbox("<br>")
        start = self.page.add_button("Start Data Collection", self.on_start_click)
        stop = self.page.add_button("End Data Collection", self.on_stop_click)
        self.txt = self.page.add_button("<br>")
        space = self.page.add_textbox("<br><br>")
        status_box = self.page.add_textbox("RFID Data Collection Status:", "h2")
        status = self.page.add_textbox("<p>\n</p>", "p")
        status.set_text("<p style=\"color:grey;\">Checking Status...</p>")
        time.sleep(1)
        while True:
            status.set_text(self.get_rf_status())
            time.sleep(0.5)

    def on_start_click(self):
        logging.info("Start RFManager")
        self.txt.set_text('<p style=\"color:green;\" font-style: italic;>Starting Data Collection...</p>')
        subprocess.call('./start_collection.sh', shell=True)
        self.txt.set_text('<br>')

    def on_stop_click(self):
        logging.info("Stop RFManager")
        self.txt.set_text('<p style=\"color:blue;\" font-style: italic;>Ending Data Collection...</p>')
        subprocess.call('./end_collection.sh', shell=True)
        self.txt.set_text('<br>')

    def get_rf_status(self):
        (code, message) = RFStatusCheck.report_status()
        logging.info('rf_status: %d | %s' % (code, message))
        return "<p style=\"color:%s;\">%s</p>" % (self.code_color[code], message)

    def main(self):
        self.main_menu()
        self.ui.done()

def main():
    setup_logger(log_file, True, False)
    ui = RFServerUI()
    ui.main()

if __name__ == '__main__':
    main()

