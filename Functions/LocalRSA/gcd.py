def greatestCommonDivisor(a, b):
    if b:
        return greatestCommonDivisor(b, a % b)
    else:
        return a


'''
扩展欧几里的算法
计算 ax + by = 1中的x与y的整数解（a与b互质）
'''


def ext_GreatestCommonDivisor(a, b):
    if b:
        r, x1, y1 = ext_GreatestCommonDivisor(b, a % b)
        x = y1

        # python3 版本中，普通的整数计算会得到精确的小数结果，
        # 因此需要把普通的/ 除法运算符换为 带有floor 效果的 //运算符
        # 但是在py2版本中，默认的计算是有舍弃小数部分的效果的
        y = x1 - a // b * y1
        return r, x, y
    else:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
