# -*- coding:utf-8 -*-
# import base64
# s = b"12345678"
# print(base64.b64encode(s))

content = ""

import time
vars = {}
print(1)
a = time.time()
code = compile(content, '<string>', 'exec')
print(2)
exec(content, vars, vars)
print(3)
output = vars['main']()
print("output", output)
print(time.time() - a)
