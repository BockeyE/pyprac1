import pymongo
from ssl import CERT_REQUIRED
import math
import re
import sha3

from RestrictedPython.forChain.limit_global import safe_globals

gs = globals()
lc = locals()


def get_safe_globals():
    safe_globals['pymongo'] = gs['pymongo']
    safe_globals['CERT_REQUIRED'] = gs['CERT_REQUIRED']
    safe_globals['math'] = gs['math']
    safe_globals['re'] = gs['re']
    safe_globals['sha3'] = gs['sha3']
    return safe_globals


with open('fullc.py', 'r', encoding='UTF-8') as f:
    meta2 = f.read()

safe_globals = get_safe_globals()
compile(meta2, '<string>', 'exec')
gs.pop('f')
exec(meta2, safe_globals)
print('safe main', safe_globals['main']())
