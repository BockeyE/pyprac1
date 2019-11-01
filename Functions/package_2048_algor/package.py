# 打包算法
def package(p):
    # 如果是奇数，则直接返回1
    if p % 2 == 1:
        print("ended with 1")
        return 1
    # 不是奇数，即为偶数时，
    # 当 & 作为位运算时，1 & 1 = 1 ，1 & 0 = 0，0 & 0 = 0；
    # 这一步计算的原因是，当一个数本身就是2的整幂次时，p & (p - 1)，是10000，01111，类似形式，这样的话可以直接返回自身
    if p & (p - 1) == 0:
        while p > 512:
            p = p - 512
        print("ended with power", p)
        return p

    # 找到最近的2幂
    # & ：按位与操作，只有1 & 1为1，其他情况为0。可用于进位运算。
    # | ：按位或操作，只有0 | 0为0，其他情况为1。
    def get_power(q):
        q = q - 1
        q = q | (q >> 16)
        q = q | (q >> 8)
        q = q | (q >> 4)
        q = q | (q >> 2)
        q = q | (q >> 1)
        return q + 1

    m = get_power(p) >> 1
    # m是比输入参数小的，最大2幂值，输入20，得到m是16
    print(m)
    p = p - m
    return package(p)


print(package(20))
print("&&& ", (5 & 4))
