def package(p):
    if p % 2 == 1:
        return 1
    if p & (p - 1) == 0:
        while p > 512:
            p = p - 512
        print(p)
        return p
    print(p)
    p = p - 1
    print(p)
    p = p | (p >> 16)
    print(p)
    p = p | (p >> 8)
    p = p | (p >> 4)
    p = p | (p >> 2)
    p = p | (p >> 1)
    print(p + 1)


package(14)
package(18)
