import datetime
import json
import os
import sys

from win_util import WinUtil

CONFIG = "test.json"


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def write_file(file_name, text, mode):
    f = open(file_name, mode)
    f.write(text)
    f.close()


def read_file(file_name):
    f = open(file_name)
    text = f.read()
    f.close()
    return text


def run(file_name, test_code, imperson):
    try:
        delete_file(file_name)
        write_file(file_name, test_code, "w")
        raise Exception("Target is not protected.")
    except:
        pass
    util = WinUtil(imperson)
    util.open()
    try:
        delete_file(file_name)
        write_file(file_name, test_code, "w")
        text = read_file(file_name)
        if test_code not in text:
            raise Exception("Failed.")
    finally:
        util.close()


try:
    with open(CONFIG) as app_config_json:
        app_config = json.load(app_config_json)
    file_name = app_config["file_name"]
    test_code = app_config["test_code"]
    imperson = app_config["imperson"]
    run(file_name, test_code, imperson)
    print("Success!")
except Exception as e:
    print(e)
    print("Failed!")
