import logging
import os
import subprocess
import time
import json

from piui import PiUi

import RFStatusCheck

ui = PiUi()
page = ui.new_ui_page(title="RFConnect")
log_file = 'RFServer/log/rfserver.log'

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
        self.page = None
        self.title = None
        self.txt = None
        self.status_head = None
        self.status_txt = None
        self.action_txt = None
        self.download_title = None
        self.download_link = None
        self.img = None
        self.ui = PiUi()
        self.src = None
        self.rfstatus = RFStatusCheck.RFStatusCheck()

        self.status_states = {
            0 : '<p style=\"color:SlateGray;font-style:italic;\">Checking Status...</p>',
            1 : '<p style=\"color:blue;font-weight:normal;\">Waiting to scan inventory.</p>',
            2 : '<p style=\"color:LimeGreen;font-weight:bold;\">Inventory scan in progress.</p>',
            3 : '<p style=\"color:blue;font-weight:bold;\">Inventory scan completed successfully.</p>',
            4 : '<p style=\"color:red;font-weight:bold;\">Inventory scan failed.</p>'
        }

        self.action_states = {
            0 : '<p>&nbsp;</p>',
            1 : '<p style=\"color:SlateGray;font-style:italic;\">Starting Data Collection...</p>',
            2 : '<p style=\"color:DarkSlateGray;font-weight:normal;\">Inventory scan is already running.</p>',
            3 : '<p style=\"color:SlateGray;font-style:italic;\">Stopping Data Collection...</p>',
            4 : '<p style=\"color:DarkSlateGray;font-weight:normal;\">Inventory scan is not running.</p>'
        }
        self.status_state = 0
        self.action_state = 0

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="RFConnect")
        self.title = self.page.add_textbox("RFID Inventory Scan", "h1")
        self.page.add_textbox("<br>", "p")
        start = self.page.add_button("Start Data Collection", self.on_start_click)
        self.page.add_textbox(self.action_states[0], "p")
        stop = self.page.add_button("End Data Collection", self.on_stop_click)
        self.action_txt = self.page.add_textbox("<br>", "p")
        self.page.add_textbox("<br>", "p")
        self.download_title = self.page.add_textbox("<p></p>", "h2")
        self.download_link = self.page.add_textbox("<a></a>", "a")

        self.page.add_textbox("RFID Data Collection Status:", "h2")
        self.status_title = self.page.add_textbox("<p>&nbsp;<p>", "p")
        self.status_txt = self.page.add_textbox("<br>", "p")
        self.status_state = 0
        self.action_state = 0
        time.sleep(1)
        while True:
            self.refresh_state()
            time.sleep(1)

    def refresh_action_state(self):
        action = self.action_state

        if action is 0:
            pass

        elif action is 1:
            if self.status_state is 2:
                self.action_state = 0

        elif action is 2:
            pass

        elif action is 3:
            if self.status_state is 3 or self.status_state is 4:
                self.action_state = 0
        elif action is 4:
            pass

        self.action_txt.set_text(self.action_states[self.action_state])

    def refresh_state(self):
        status = self.update_status_state()
        self.status_title.set_text(self.status_states[self.status_state])
        text = '<br>'

        if status is 0:
            text = '<br>'

        elif status is 1:
            text = '<br>'

        elif status is 2:
            # show tags in a table as they come in
            text = '<p>Started: %s</p>' % self.rfstatus.read_start_time()
            text += '<p>Current runtime: %d minutes, %d seconds</p>' % self.rfstatus.calculate_runtime()
            if self.rfstatus.has_written_file('.json'):
                #print tag progress
                text += '<br><p>RFID Tags Captured:</p>'
                text += self.build_tag_table()

        elif status is 3:
        # retrieve output file
            text = '<p>Started: %s</p>' % self.rfstatus.read_start_time()
            text += '<p>Runtime: %d minutes, %d seconds</p>' % self.rfstatus.calculate_final_runtime()
            if self.rfstatus.has_written_file('.json'):
                # print tag progress
                text += '<br><p>RFID Tags Captured:</p>'
                text += self.build_tag_table()

            #if self.rfstatus.has_written_file('.xlsx'):
            #   self.download_title.set_text('Inventory Scan Report')
            #    dl_path = self.resolve_dl_path('.xlsx')
            #    dl_element = '<a href=\"%s\" download>Click to download</a>' % dl_path
            #    self.download_link.set_text(dl_element)

        elif status is 4:
        # display error
            text = '<p>Details: %s</p>' % self.rfstatus.read_error()

        self.refresh_action_state()
        self.status_txt.set_text(text)

    def on_start_click(self):
        logging.info('Start button clicked')

        #if inventory scan already running
        if self.status_state is 2:
            self.action_state = 2
        else:
            self.action_state = 1
            self.refresh_action_state()
            logging.info("executing: \'./start_collection.sh\'")
            subprocess.call('./start_collection.sh', shell=True)
        self.refresh_state()

    def on_stop_click(self):
        logging.info('Stop button clicked')

        # if inventory scan not running
        if self.status_state is not 2:
            self.action_state = 4
        else:
            self.action_state = 3
            self.refresh_action_state()
            logging.info("executing: \'./end_collection.sh\'")
            subprocess.call('./end_collection.sh', shell=True)
        self.refresh_state()


    def update_status_state(self):
        state = self.rfstatus.check_rf_state()
        self.status_state = state
        return state

    def build_tag_table(self):
        table = '<table style=\"width:100%\" border="1">'
        try:
            json_file = self.rfstatus.read_file_name('.json')
            logging.info("json file: %s" % json_file)
            json_data = self.rfstatus.read_tag_file(json_file)
            logging.info ("json: %s" % json_data)
            tag_map = json.loads(json_data)['RF Tags Identified']['data']

            table += '<tr><th>Tag ID</th><th>Time Last Seen</th></tr>'
            for tag in tag_map:
                table += '<tr><td>' + str(tag) + '</td><td>' + str(tag_map[tag]) + '</td></tr>'
            table += '</table>'
            return table
        except:
            return '<p>unable to create tags table</p>'

    def resolve_dl_path(self, extension):
        filename = self.rfstatus.read_file_name(extension)
        return self.rfstatus.get_scan_data_path() + filename

    def main(self):
        self.main_menu()
        self.ui.done()

def main():
    setup_logger(log_file, True, False)
    ui = RFServerUI()
    ui.main()

if __name__ == '__main__':
    main()

