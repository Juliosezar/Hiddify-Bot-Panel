from persiantools.jdatetime import JalaliDateTime
from uuid import UUID
import json
from datetime import datetime

def now_timestamp():
    return int(JalaliDateTime.now().timestamp())

def now_date():
    return datetime.now().strftime("%Y-%m-%d")

def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def args_spliter(args):
    return args.split("<%>")



def generate_unique_name():
    with open("settings.json", "r+") as f:
        setting = json.load(f)
        counter = setting["config_name_counter"]
        setting["config_name_counter"] += 1
        f.seek(0)
        json.dump(setting, f)
        f.truncate()
        return "NapsV_" + str(counter)
