from persiantools.jdatetime import JalaliDateTime
from uuid import UUID
def now_timestamp():
    return int(JalaliDateTime.now().timestamp())

def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def command_spliter(args):
    return args.split("<%>")