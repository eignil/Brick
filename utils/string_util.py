import print_util

def _try_decode(ori_str,encoding):
    try:
       decode_str = ori_str.decode(encoding)
       return decode_str
    except Exception as ex:
        print_util.print_std(ex)
        return ex

def decode_chs_str(ori_str):
    try_encoding = ['utf-8','gbk','gb2312','gb18030','hz']
    for encoding in try_encoding:
        res = _try_decode(ori_str,encoding)
        if not isinstance(res,Exception):
            return res
        else:
            continue
    return ori_str