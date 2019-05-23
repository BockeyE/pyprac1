import builtins

# from RestrictedPython.Guards import safe_globals
import requests
import os
import math
import builtins

cmd = '''
a=math.sqrt(4)
print(a)
print(' ==========')
print(dir())
print(globals())
print(' ==========')
'''

print(dir())

print('exec>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
exec(cmd, )
print('exec end<<<<<<<<<<<<<<<<<<<<<<<<<<')

print(dir())
print(globals())
# print(gs.get('__builtins__'))
# print(gs.get('builtins'))
# # print(getattr(builtins, 'builtins'))
# print(builtins)

'''['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'builtins', ]'''
'''['__builtins__', '__import__', 'pOperationFailure', 're']
'''
