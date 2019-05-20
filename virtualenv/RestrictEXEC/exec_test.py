# python_source = '''
# def func():
#   print('in func')
# print(dir())
# a = 5
# print(dir())'''
# global_namespace = {}
# local_namespace = {}
# exec(python_source, global_namespace, local_namespace)
# a = local_namespace['a']  # 通过字典查找变量
# # func = global_namespace['func']# 报错
# func = local_namespace['func']  # 通过字典查找函数
# # func = global_namespace['func']# 报错
# print(a)  # 打印出函数的地址空间
# func()


import math

exec('print(dir())', {})
# ['func']
# ['a', 'func']
# 5
# in func


from math import *

exec('print(dir())', {'squareRoot': sqrt, 'pow': pow})


def no(**kwargs):
    pass


# object can have squareRoot() module
# exec('print(squareRoot(9))', {'squareRoot': sqrt, 'pow': pow})
# 下面的话会报异常
# exec('print(sqrt(9))', {'sqrt': sqrt, 'pow': pow})
exec('exec(\'print(sqrt(9))\')', {'sqrt': no, 'pow': pow})

'''用户不传递globals字典时，默认会传递一个字典(是什么不知道，应该是当前的全局变量、函数和内置函数)。
用户只传递globals字典时，如果传递空字典，exec内只能访问内置函数(__builtins__)
用户只传递globals字典时，如果传递非空字典，exec内只能访问内置函数(__builtins__)、字典中包含的函数和变量（变量只是一个拷贝，内部修改了不会影响外面的变量，外面修改了不会影响内部的变量）。
用户同时传递globals字典和locals字典时，使用方式同上，但是如果globals字典设置{'\_\_builtins\_\_' : None}，locals字典设置其他函数和方法是，就不能访问内置函数(__builtins__)。注：这一点有点疑问！

执行之后exec语句中的func和var会以字典形式存在locals中

exec执行的字符串中定义了函数和变量，是会保存在传递进去的globals字典中的，所以可以使用该字典获取字符串内的函数，并调用。
同时传递globals字典和locals字典时，locals字典优先级高。
'''
