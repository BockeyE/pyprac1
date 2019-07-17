from multiprocessing.dummy import Pool as ThreadPool


def te(adds, a2):
    c = adds + a2
    return c


pool = ThreadPool(5)
res = pool.map(te, [['111', 'a2'], ['111', 'a2'], ['111', 'a2']])
pool.close()
pool.join()
print(res)

# 多参数问题
# python中，第一个参数是*arg，第二个是**kwargs，也就是说，第一个参数是位置参数，第二个是关键字kw参数，
# 因此第一个传列表，第二个传dict字典，都可以实现多参数的效果
lst_vars_1 = ['1', '2', '3']
lst_vars_2 = ['4', '5', '6']
func_var = [(lst_vars_1, None), (lst_vars_2, None)]
# 方法2
dict_vars_1 = {'m': '1', 'n': '2', 'o': '3'}
dict_vars_2 = {'m': '4', 'n': '5', 'o': '6'}
func_var = [(None, dict_vars_1), (None, dict_vars_2)]

pool = threadpool.ThreadPool(2)
requests = threadpool.makeRequests(hello, func_var)
[pool.putRequest(req) for req in requests]
pool.wait()