import sys

def print_std(args):
    if not isinstance(args,str):
        args = str(args)
    str_print = "\r\n"+args+"\r\n"
    #print(str_print)
    #sys.__stdout__.write(str_print)
    sys.__stderr__.write(str_print)


