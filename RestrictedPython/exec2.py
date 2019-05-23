import math

with open('fullc.py', 'r', encoding='UTF-8') as f:
    meta2 = f.read()
# safe_globals['os'] = None
# print(safe_globals)

cmd = '''
with open('a.txt', 'r', encoding='UTF-8') as f:
    meta = f.read()
print(meta)
print(dir())
'''
cmd2 = '''
import math
x=math.sqrt(4)
print(x)
'''
cmd3 = '''
import math
x=sqrt(4)
print(x)
print(A(1, 2))
'''

res = {}


class A(object):
    def __init__(self, s, a):
        self.a = a
        self.s = s

    def __str__(self):
        return str(self.s) + str(self.a)


z = A(4, 5)
# print(A(1, 2))
# print(z)

# 传递一个类进去也可以
# exec(cmd3, {'sqrt': math.sqrt, 'A': A})


# exec(cmd3, {'sqrt': math.sqrt, 'A': A})

cmd4 = '''
a=1
if __name__ == '__main__':
    a=3
print(a)

'''
exec(cmd4, {'sqrt': math.sqrt, 'A': A})