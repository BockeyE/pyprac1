import pymongo.errors
import pymongo
from ssl import CERT_REQUIRED
from RestrictedPython.Guards import safe_globals

gs = globals()
print(gs)
with open('fullc.py', 'r', encoding='UTF-8') as f:
    meta2 = f.read()

compile(meta2, '<string>', 'exec')

print(safe_globals)
# safe_globals['__name__'] = gs['__name__']
# safe_globals['__doc__'] = gs['__doc__']
# safe_globals['__package__'] = gs['__package__']
# safe_globals['__loader__'] = gs['__loader__']
# safe_globals['__annotations__'] = gs['__annotations__']
# safe_globals['__spec__'] = gs['__spec__']
safe_globals['pymongo'] = gs['pymongo']
# gs['__builtins__'] = safe_globals['__builtins__']
# gs.pop('__name__')
# gs.pop('__doc__')
# gs.pop('__package__')
# gs.pop('__loader__')
# gs.pop('__annotations__')
# gs.pop('__spec__')
# gs.pop('safe_globals')
gs.pop('f')
print(gs)
print('go exec >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
exec(meta2, safe_globals)
