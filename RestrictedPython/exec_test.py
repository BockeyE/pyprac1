import pymongo.errors
import pymongo
from ssl import CERT_REQUIRED
from RestrictedPython.Guards import safe_globals
import math
import re
import sha3
gs = globals()
print(gs)
with open('fullc.py', 'r', encoding='UTF-8') as f:
    meta2 = f.read()

compile(meta2, '<string>', 'exec')
safe_globals['pymongo'] = gs['pymongo']
safe_globals['CERT_REQUIRED'] = gs['CERT_REQUIRED']
safe_globals['math'] = gs['math']
safe_globals['re'] = gs['re']
safe_globals['sha3'] = gs['sha3']
gs.pop('f')
exec(meta2, safe_globals)
print(safe_globals['main']())
