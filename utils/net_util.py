from platform   import system as system_name  # Returns the system/OS name
import subprocess  # Execute a shell command
from multiprocessing.dummy import Pool as ThreadPool
import print_util
import string_util

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    If on windows,can set CMD encoding to UTF-8 with "chcp 65001" 
    """
    
    # Ping command count option as function of OS
    param = '-n' if system_name().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    streamdata = process.communicate()[0]
    #print_util.print_std(streamdata)
    streamdata = string_util.decode_chs_str(streamdata)
    print_util.print_std(streamdata)
    if system_name().lower()=='windows':
        #On windows use this to check ping pass or fail.
        if 'TTL='   in str(streamdata):
            return True
        else:
            return False
    return process.returncode==0

def ping_success(host):
    assert  ping(host)

def ping_fail(host):
    assert not ping(host)

def pings(hosts):
    #Ping with multi process
    host_num = len(hosts)
    if host_num >5:
        thread_num = 5
    else:
        thread_num = host_num
    pool  = ThreadPool(thread_num)
    results = pool.map(ping, hosts)
    for ele in results:
        if not ele:
            return False
    return True