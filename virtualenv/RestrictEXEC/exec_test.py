python_source = '''
def func():
  print('in func')
print(dir())
a = 5
print(dir())'''
global_namespace = {}
local_namespace = {}
exec(python_source, global_namespace, local_namespace)
a = local_namespace['a']  # 通过字典查找变量
# func = global_namespace['func']# 报错
func = local_namespace['func']  # 通过字典查找函数
# func = global_namespace['func']# 报错
print(a)  # 打印出函数的地址空间
func()

# ['func']
# ['a', 'func']
# 5
# in func
