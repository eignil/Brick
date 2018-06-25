#from collections import namedtuple

def split_into_lines(multilines,sep="\n",do_strip=True):
        multilines_list = multilines.split(sep)
        if do_strip:
            multilines_list = [ele.strip() for ele in multilines_list if ele.strip()]
        return multilines_list
    
def split_into_table(res,col_sep=":",row_sep="\n",do_strip=True):
    '''

    '''
    lines = split_into_lines(res,row_sep,do_strip)
    lines_table = []
    for line in lines:
        spl = line.split(col_sep,1)
        if do_strip:
            spl = [ele.strip() for ele in spl if ele.strip()]
        if len(spl)>0:
            lines_table.append(spl)
    return lines_table