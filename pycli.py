import sys
import logging
from pexpect import TIMEOUT
import serial
if sys.platform == 'win32':
    from .pexpect_serial.pexpect_serial import SerialSpawn
else:
    raise Exception("Only support windows")
import time
import re
from datetime import datetime,timedelta

from enum import Enum



class EnvType(Enum):
    NotLogin = 0
    Login    = 1
    Linux    = 2

class ResType(Enum):
    RawExpect = 0
    ParsedExpect = 1
    ParsedCli = 2
    Text = 3


class PyCli(object):
    def __init__(self,conn):
        self.prompt_end = {'>':EnvType.NotLogin,'->':EnvType.Login,'#':EnvType.Linux}
        self.init_logger()
        self.conn = conn

    def init_logger(self):
        log_format_str = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        logging.basicConfig(format=log_format_str)
        self.logger = logging.getLogger("PyCli")
        self.logger.setLevel(logging.DEBUG)

    
    def get_current_prompt(self,is_origin=False):
        res = self.conn.sync_original_prompt(1)
        if not res:
            raise Exception("Didn't get original prompt")
        #print("get_current_prompt",res)
        res = res.strip().decode()
        if not res:
            raise Exception("Can't get unique prompt!")
        else:
            if not is_origin:
                #Fix the session timeout problem.
                if len(res)>=2 and res[-2:]=="->":
                    res = res[0:-2]+"-?>"
            self.logger.info("Current prompt:%s"%(res))
            self.current_prompt = res
            self.conn.set_prompt(res)
        return res

    def get_response(self):
        return [self.conn.before, self.conn.after]


    def format_command(self,command,is_shown=True):
        if isinstance(command,str):
            command = command.lstrip().rstrip()
        elif isinstance(command,list) or isinstance(command,tuple):
            command = " ".join(command)
        else:
            raise Exception("Command is not string")
        if is_shown:
            self.logger.info(command)
        return command
        

    def run_command(self,command,expect=None,prompt=None,is_line=True,is_shown=True):
        '''
        The response will be split into an array.One element is a line of the response.
        '''
        try:
            command = self.format_command(command,is_shown=is_shown)
            
            if is_line:
                self.conn.sendline(command)
            else:
                self.conn.send(command)
            if expect:
                self.conn.expect(expect)
            else:
                if prompt:
                    old_prompt = self.conn.get_prompt()
                    self.conn.set_prompt(prompt)
                    self.conn.prompt()
                    self.conn.set_prompt(old_prompt)
                else:
                    self.conn.prompt()
            return (self.conn.before,self.conn.after)
        except Exception as ex:
            self.logger.error(ex)
            return None

    def run_command_steps(self,command,expects=None,inputs=None,expect=None,prompt=None,is_shown=True):
        '''
        Some commands need input parameter step by step.
        expect: The last expect.
        '''
        if len(expects) > len(inputs) :
            raise Exception ("Invalid expects and inputs.")

        command = self.format_command(command,is_shown)
        res = []
        self.conn.sendline(command)
        if inputs:
            if len(inputs) != len(expects):
                raise Exception("Invalid inputs and expects")
            for idx,input_val in enumerate(inputs):
                expect_val = expects[idx]
                if expect_val and isinstance(expect_val,str):
                    expect_val = [expect_val,self.conn.get_prompt(),TIMEOUT]
                    index = self.conn.expect(expect_val)
                    res.append(self.conn.before)
                    res.append(self.conn.after)
                    if index !=0:
                        return res
                else:
                    if expect_val >0:
                        wait_time = expect_val
                    else:
                        wait_time = 0.5
                    time.sleep(wait_time)
                self.conn.sendline(input_val)
        if expect:
            self.conn.expect(expect)
        else:
            if prompt:
                old_prompt = self.conn.get_prompt()
                self.conn.set_prompt(prompt)
                self.conn.prompt()
                self.conn.set_prompt(old_prompt)
            else:
                self.conn.prompt()
        res.append(self.conn.before)
        res.append(self.conn.after)
        return res

    @classmethod
    def uart_conn_init(cls, 
                 port=None,
                 baudrate=9600,
                 bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 timeout=10,
                 xonxoff=False,
                 rtscts=False):
        s = serial.Serial(port=port,baudrate=baudrate,bytesize=bytesize,parity=parity,
                    stopbits=stopbits,xonxoff=xonxoff,rtscts=rtscts)
        conn = SerialSpawn(s,timeout=timeout,maxread=4000)
        conn.set_linesep('\n')
        return conn

    def print_res(self,response):
        print("\n")
        if isinstance(response,list) or isinstance(response,tuple):
            print("\n".join(response))
        else:
            #self.logger.info(str(response))
            print(str(response))


if __name__ == '__main__':
    print("Starting...")
    conn = PyCli.uart_conn_init("COM4",38400)
    ins = PyCli(conn)
    print(ins.get_current_prompt())