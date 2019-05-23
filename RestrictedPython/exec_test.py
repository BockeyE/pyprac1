import pymongo.errors
import pymongo
from ssl import CERT_REQUIRED
from RestrictedPython.Guards import safe_globals

with open('fullc_clear.py', 'r', encoding='UTF-8') as f:
    # with open('fullc.py', 'r', encoding='UTF-8') as f:
    meta2 = f.read()

mylocals = {'AutoReconnect': pymongo.errors.AutoReconnect,
            'DuplicateKeyError': pymongo.errors.DuplicateKeyError,
            'pOperationFailure': pymongo.errors.OperationFailure,
            'MongoClient': pymongo.MongoClient,
            'ConnectionFailure': pymongo.errors.ConnectionFailure,
            'ConfigurationError': pymongo.errors.ConfigurationError,
            'CERT_REQUIRED': CERT_REQUIRED,
            '__import__': None}

gs = globals()
# my = {}
my = gs
safe_globals['__loader__'] = gs['__loader__']
safe_globals['__builtins__'] = gs['__builtins__']
compile(meta2, '<string>', 'exec')
exec(meta2, mylocals)
# print(my)
# print(my['main']())
