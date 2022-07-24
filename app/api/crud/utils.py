from datetime import datetime
import pytz
import random
import string
import uuid

def return_only_number(param):
    return ''.join(filter(str.isdigit, param))


def generate_request_no(code):
    date_time = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y%m%d")
    fuuid = str(uuid.uuid4()).split('-')[0]
    return f'{code}-{date_time}-{fuuid}'


def random_alphanumeric(size):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


def clean_dictionary(obj):
    param = obj
    filtered = {k: v for k, v in param.items() if v is not None}
    param.clear()
    param.update(filtered)
    return param
