import json
import os

def get_board_conf(conf_path=os.path.join(os.getcwd(),"board_conf.json")):
    f = open(conf_path,'r')
    return json.load(f)


def get_test_users():
    conf = get_board_conf()
    users = conf["test_users"]
    return users

def test_get_admin_user():
    users = get_test_users()
    return users[2]