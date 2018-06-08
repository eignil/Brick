import time

def measure_time(this_log=print):
    '''
    wrap a function to wait that function return expect value.
    If rounds is 0, there is no rounds limitation.
    If rounds is given, timeOutInseconds will be ignore.
    The w
    '''
    if not this_log:
        def _this_log(*args,**kwargs):
            pass
        this_log = _this_log
    def decorator(func):
        def _inner_func(*args,**kargs):
            start_time = time.time()
            try:
                res = func(*args,**kargs)
            except Exception as ex:
                res = ex
                pass
            cost_time = time.time()-start_time
            this_log("%s Cost time %f"%(func.__name__,cost_time))
            return res
        return _inner_func
    return decorator

    