*** settings ***
Library    brick.pycli_robot_lib
Test Setup      open uart    COM4    38400
#Test Teardown    Close Application

*** Test Cases ***
test login linux
    sendline    \n
    expect      localhost login:
    sendline    root
    expect      Password:
    sendline    root

