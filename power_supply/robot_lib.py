import sys
from robot.api.deco import keyword
from robot.version import get_version,get_full_version
from brick.power_supply.psw import PswConn
#from psw import PswConn

def print_std(args):
    sys.__stdout__.write(args+"\n")

class PswRun(PswConn):
    

    def __init__(self,*args):
        super(PswRun,self).__init__(*args)

    def run_keyword(self,name,*args):
        whole_cmd = name

        for arg in args[0:-1]:
            whole_cmd+=":"+str(arg)
        last_arg = args[-1]
        if last_arg == '?':
            whole_cmd+=last_arg
        else:
            whole_cmd+=" "+str(last_arg)
        print_std("run command:%s"%(whole_cmd))
        res = self.send_command_read_response(whole_cmd+"\n")
        print_std(res)
        return res

    def __getattr__(self,name):
        self._cur_keywork = name
        def run(*args):
            return self.run_keyword(name,*args)
        setattr(run,"ROBOT_LISTENER_API_VERSION",3)
        return run

class Psw(object):
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'
    ROBOT_LIBRARY_VERSION = get_version()
    

    keywords = ['setup connect','*IDN','APPLy','OUTPut','SYSTem','MEASure','SOURce']
    def __init__(self, uart_port, baudrate=9600):
        self._conn = self._get_connection(uart_port,baudrate)

    #def open_connection(self,)
    
    def _get_connection(self, *args):
        """Can be overridden to use a custom connection."""
        self._conn = PswRun(*args)
        return self._conn

    def get_keyword_names(self):
        return Psw.keywords

    def __getattr__(self, name):
        return getattr(self._conn or self._get_connection(),name)
