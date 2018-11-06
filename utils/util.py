import sys
import random
import json
import time
import sys
import time


from robot.api import logger

def split_into_lines(multilines,sep="\n"):
    multilines_list = multilines.split(sep)
    multilines_list = [ele.strip() for ele in multilines_list if ele.strip()]
    return multilines_list
    
def split_lines_into_dict(lines,col_sep=":"):
    lines_table = {}
    cur_dict = None
    for line in lines:
        spl = line.split(col_sep,1)
        spl = [ele.strip() for ele in spl if ele.strip()]
        if len(spl)==0:
            continue
        #New sub dict
        if len(spl)==1 :
            if not cur_dict:
                cur_dict = (spl[0],{})
            else:
                lines_table[cur_dict[0]] = cur_dict[1]
                cur_dict = (spl[0],{})
        if len(spl)==2:
            if cur_dict:
                cur_dict[1][spl[0]] = spl[1]
            else:
                lines_table[spl[0]] = spl[1]
        else:
            raise  Exception("Invalid table")
    return lines_table


def parse_table_without_header(table_arr,split_line=None):
    if not split_line:
        def _split_line(line):
            line = line.split(" ")
            line = [ele.strip() for ele in line if ele.strip()]
            return line
        split_line = _split_line
    lines = table_arr
    lines_vals = []
    for line in lines:
        cols = split_line(line)
        lines_vals.append(cols)
    return lines_vals

def parse_table(table_arr,line_type_name="Line",split_line=None):
    if not split_line:
        def _split_line(line):
            line = line.split(" ")
            line = [ele.strip() for ele in line if ele.strip()]
            return line
        split_line = _split_line
    headers = split_line(table_arr[0])
    headers = [ele.strip() for ele in headers]
    lines = table_arr[1:]
    lines_vals = []
    for line in lines:
        line_val = namedtuple(line_type_name,headers)
        cols = split_line(line)
        lines_vals.append(line_val(*cols))
    return lines_vals






def cast_float_prec(origin_float,resolution):
    res = str(resolution).split('.')
    if len(res)>0:
        prec = len(res[1])
    else:
        prec = 0
    gened = round(origin_float,prec)
    return gened


def gen_random_float_prec(resolution):
    return cast_float_prec(random.uniform(1,100),resolution)

def start_time():
    return time.time()

def get_elapsed_time(start_time):
    return time.time() - int(start_time)


