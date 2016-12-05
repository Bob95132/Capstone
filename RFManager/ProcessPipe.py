import pexpect
import time

class ProcessPipe:
    def __init__(self, command, user=None, expect=None, timeout=0.1):
        self.command = command
        self.returnCode = None
        self.response = None
        self.timeout = float(timeout)
        if user is not None:
            self.command = 'su - ' + user + ' -c \"' + self.command + '\"'
        self.process = self.start_process()
        if expect is not None:
            self.expect(expect)
        else:
            self.no_expect()

    #spawn child process
    def start_process(self):
        return pexpect.spawn(self.command)

    #expect these strings in child's output stream
    def expect(self, *matches):
        expects = []
        for match in matches:
            expects.append(match)
        expects.append(pexpect.EOF)
        expects.append(pexpect.TIMEOUT)

        index = self.process.expect(expects, timeout=self.timeout)
        if index > len(expects) - 3:
            self.response = self.process.before
            return -1
        else:
            self.response = self.process.after
            return index

    #capture full output stream on timeout
    def no_expect(self):
        self.process.expect(pexpect.TIMEOUT, timeout=self.timeout)
        self.response = self.process.before

    #take list of strings and convert to string
    def parse_args(self, args):
        arg_str = ''
        if isinstance(args, list):
            for arg in args:
                arg_str += arg
                arg_str += ' '
            if len(arg_str):
                arg_str -= ' '

        else:
            arg_str = args

        return arg_str


    #send command line to child's stdin
    def sendline(self, args):
        try:
            str = self.parse_args(args)
            self.process.sendline(str)
        except:
            if self.process.isalive():
                return -1
            else:
                print 'dead'
                return 1
