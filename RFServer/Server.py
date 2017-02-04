from piui import PiUi
import RFStatusCheck
import os
import subprocess
import time

ui = PiUi()
page = ui.new_ui_page(title="RFConnect")
title = page.add_textbox("Hello, world!")

current_dir = os.path.dirname(os.path.abspath(__file__))

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
        space = self.page.add_textbox("<p></p>", "h1")
        start = self.page.add_button("Start Data Collection", self.on_start_click)
        stop = self.page.add_button("End Data Collection", self.on_stop_click)
        space = self.page.add_textbox("<p>\n\n</p>", "h1")
        status_box = self.page.add_textbox("RFID Data Collection Status:", "h2")
        status = self.page.add_textbox("<p>\n</p>", "p")
        status.set_text("<p style=\"color:grey;\">Checking Status...</p>")
        time.sleep(1)
        while True:
            status.set_text(self.get_rf_status())
            time.sleep(0.5)

    def on_start_click(self):
        print "Start RFManager"
        subprocess.call('./start_collecton.sh')

    def on_stop_click(self):
        print "Stop RFManager"
        subprocess.call('./end_collection.sh')

    def get_rf_status(self):
        (code, message) = RFStatusCheck.report_status()
        return "<p style=\"color:%s;\">%s</p>" % (self.code_color[code], message)

    def main(self):
        self.main_menu()
        self.ui.done()

def main():
    ui = RFServerUI()
    ui.main()

if __name__ == '__main__':
    main()