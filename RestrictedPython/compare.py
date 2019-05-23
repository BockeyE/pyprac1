import builtins

# from RestrictedPython.Guards import safe_globals
import requests
import os
import math

cmd = '''
a=math.sqrt(4)
print(a)
print(dir())
'''

exec(cmd, )
# print(dir())
gs = globals()
print(gs)

'''
{'__name__': '__main__', 
'__doc__': None, 
'__package__': None, 
'__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x0000028F08798080>, 
'__spec__': None, 
'__annotations__': {}, 
'__builtins__': <module 'builtins' (built-in)>, 
'__file__': 'C:/ZZBK/persontest/test1/mysite/RestrictedPython/compare.py', 
'__cached__': None, 
'builtins': <module 'builtins' (built-in)>, 
'requests': <module 'requests' from 'C:\\py367\\Python\\Python36\\Lib\\site-packages\\requests\\__init__.py'>, 
'os': <module 'os' from 'C:\\py367\\Python\\Python36\\lib\\os.py'>, 'math': <module 'math' (built-in)>, 
'cmd': '\na=math.sqrt(4)\nprint(a)\nprint(dir())\n', 
'a': 2.0, 
'gs': {...}}


'''
