from Utils import get_property
import logging


class RFStatus():
    def __init__(self):
        self.a_codes = {}
        self.b_codes = {}
        self.load_constants()

        self.status_dir = get_property("RF_STATUS_PATH", "CONFIGS")
        self.status_file = get_property("RF_STATUS_FILE", "CONFIGS")

    def load_constants(self):
        self.a_codes['STOPPED'] = get_property("STATUS_CODE_STOPPED", "CONFIGS")
        self.a_codes['RUNNING'] = get_property("STATUS_CODE_RUNNING", "CONFIGS")
        self.a_codes['FWRITE'] = get_property("STATUS_CODE_FWRITE", "CONFIGS")

        self.b_codes['SUCCESS'] = get_property("STATUS_CODE_SUCCESS", "CONFIGS")
        self.b_codes['ERROR'] = get_property("STATUS_CODE_ERROR", "CONFIGS")

    # Create, or append a line to the RF_STATUS file
    def write_status_file(self, code_a, code_b, append_str, overwrite=False):

        try:
            if overwrite:
                fd = open(self.status_dir + self.status_file, 'w')
            else:
                fd = open(self.status_dir + self.status_file, 'a+')

            if append_str:
                fd.write(code_a + code_b + '|' + append_str + '\n')

            fd.close()

        except (OSError, IOError) as e:
            logging.error('error writing RF_STATUS file.')

    def start_status(self, timestamp, additional=None):
        append = timestamp
        if additional:
            append += '|' + additional
        self.write_status_file(self.a_codes['RUNNING'], self.b_codes['SUCCESS'], append, overwrite=True)

    def end_success(self, timestamp, additional=None):
        append = timestamp
        if additional:
            append += '|' + additional
        self.write_status_file(self.a_codes['STOPPED'], self.b_codes['SUCCESS'], append)

    def end_failure(self, additional=None):
        if not additional:
           additional = 'Unknown failure'
        self.write_status_file(self.a_codes['STOPPED'], self.b_codes['ERROR'], additional)

    def file_write(self, message, filename):
        self.write_status_file(self.a_codes['FWRITE'], self.b_codes['SUCCESS'], message + '|' + filename)
