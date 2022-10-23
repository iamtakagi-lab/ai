import random
import string
import platform
from hash import get_hash

def get_reference_code(length=10):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_version_string():
    return "🤖 ai (https://github.com/yuderobot/ai {}) on {}, {}, {}".format(get_hash(), platform.platform(), platform.python_implementation(), platform.python_version())
