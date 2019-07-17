from multiprocessing.dummy import Pool as ThreadPool
def te(adds):
    c = adds + adds
    return c


pool = ThreadPool(5)
res = pool.map(te, ['123', '33', '66'])
pool.close()
pool.join()
print(res)
