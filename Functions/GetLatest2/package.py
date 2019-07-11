def package(p):
    if p % 2 == 1:
        print("ended with 1")
        return 1
    if p & (p - 1) == 0:
        while p > 512:
            p = p - 512
        print(p)
        print("ended with power")
        return p
    m = get_power(p) >> 1
    print(m)
    package(p - m)


def get_power(p):
    p = p - 1
    p = p | (p >> 16)
    p = p | (p >> 8)
    p = p | (p >> 4)
    p = p | (p >> 2)
    p = p | (p >> 1)
    return p + 1


package(14)
package(18)
package(20)
package(24)
package(28)
package(36)
