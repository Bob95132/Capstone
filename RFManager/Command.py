#Command class for executing shell commands
import subprocess
import time
from Utils import *

class Command:
    def __init__(self, command, user=None):
        self.command = command
        self.returnCode = None
        self.stdout = None
        self.stderr = None
        if user is not None:
            self.command = 'su - ' + user + ' -c \"' + self.command + '\"'

    def execute_command(self, parse_function=None):
        logging.debug('executing command: %s' % self.command)
        p = subprocess.Popen([self.command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.stdout, self.stderr) = p.communicate()
        self.returnCode = p.returncode
        result = filter(None, self.stdout.split('\n'))
        if parse_function:
            return parse_function(result)
        else:
            return result


    def execute_command_with_retry(self, retry_handler=None, timeout=0, error_reporter=None, success_reporter=None):
        start_time = int(round(time.time()))
        call_count = 0
        retry_allowed = 0
        while retry_allowed == 0:
            try:
                response = self.execute_command(self.parse_join_list)
                if response:
                    logging.debug(response)
                if self.returnCode == 0:
                    if success_reporter:
                        success_reporter(self.command)
                    break
                else:
                    logging.debug('STDERROR RESPONSE:\n%s' % self.stderr)
            except Exception as e:
                logging.error(e.message)
            # Command failed. report error using error_reporter or logging.error
            if error_reporter:
                error_reporter(self.command)
            else:
                logging.error('command: \"%s\" failed.' % self.command)
            call_count += 1
            if retry_handler is not None:
                # use passed retry handler
                retry_allowed = retry_handler(call_count, start_time, timeout)
            else:
                # try one time
                retry_allowed = call_count if call_count > 1 else 0

        return self.returnCode

    def parse_join_list(self, lines):
        if lines:
            return 'STDOUT RESPONSE:\n' + '\n'.join(list(lines))
        else:
            return None