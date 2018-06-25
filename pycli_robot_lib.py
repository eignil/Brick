from robot.api.deco import keyword
from .pycli import *

class pycli_robot_lib(object):
    pexpect_keywords=["send","sendline","expect"]

    def __init__(self):
        self._conn_ins = None
        print(self.get_keyword_names())
        
    @keyword
    def open_uart(self,uart_port,baudrate=115200,timeout=10):
        if isinstance(baudrate,str):
            baudrate = int(baudrate)
        conn = PyCli.uart_conn_init(port=uart_port,baudrate=baudrate,timeout=timeout)
        self._conn_ins = PyCli(conn)

    def get_keyword_names(self):
        all_keywords = [name for name in dir(self) if hasattr(getattr(self, name), 'robot_name')]
        all_keywords.extend(pycli_robot_lib.pexpect_keywords)
        print(all_keywords)
        return all_keywords
    
    def excute_pexpect(self,cmd,args):
        #try:
        return getattr(self._conn_ins.conn,cmd)(*args)
        #except Exception as ex:
        #    print(ex)
        #    return ex

    def excute_keyword(self,name,args):
        whole_cmd = name
        for arg in args:
            whole_cmd+=" "+str(arg).strip()
        
        print_std(">%s"%(whole_cmd))
        print(name,args)

        start_time = time.time()
        res  =  self.send_cmd_read_res(whole_cmd)
        end_time = time.time()
        if self.check_raw_res(name,args):
            if isinstance(res,str):
                res = binascii.hexlify(res.encode()).decode()
            else:
                #print(type(res))
                #print(res)
                res = binascii.hexlify(res).decode()
            #print(res)
        print_std("%s"%(res))
        #print_std("Cost time:%f"%(end_time-start_time))
        return res

    def __getattr__(self,name):
        if name in self.pexpect_keywords:
            self._cur_keywork = name
            #print("keyword:",name)
            def run(*args):
                return self.excute_pexpect(name,args)
            setattr(run,"ROBOT_LISTENER_API_VERSION",3)

            return run