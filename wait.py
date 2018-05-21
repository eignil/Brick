
import time

def wait_for(expect=True,rounds=0,timeout=60,sleepTimeOut=5,this_log=print):
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
        def rounds_loop_func(*args,**kargs):
            is_success = False 
            start_time = time.time()
            end_time = start_time + timeout
            pre_log_time = start_time
            idx = 0
            while (idx < rounds) or (not rounds):
                idx += 1
                try:
                    res = func(*args,**kargs)
                except Exception as ex:
                    res = ex
                    pass
                else:
                    if res == expect:
                        this_log("{0} Finished in rounds:{1} time:{2} seconds".format(func.__name__,idx,time.time()-start_time))
                        is_success = True
                        break
                    
                if time.time() - pre_log_time > 5:
                    this_log("{0}, Rounds:{1} result: {2}".format(func.__name__,idx,res))
                    pre_log_time = time.time()
                if time.time()  > end_time:
                    this_log("{0} timeout in rounds:{1} time:{2} seconds".format(func.__name__,idx,time.time()-start_time))
                    break
                time.sleep(sleepTimeOut)
            print(res)
            return is_success
        return rounds_loop_func
    return decorator

    