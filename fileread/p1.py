import hashlib
import os
import re

from click._compat import raw_input

def CalcFileSha256():
    file_path = 'C:\ZZBK\sqs.pdf'
    with open(file_path, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        return hash_value

def act(fname, mark, rep, outf):
    # 打开文件，readlines是py读文本成str数组的方法
    with open(fname, 'r', encoding='UTF-8') as f:
        strs = f.readlines()

    # 遍历数组
    for p in range(len(strs)):
        # 如果以wav结束，则是一组的开始
        if strs[p].endswith(".wav\n"):
            # 拿到主体两行，设置2个标记，i，j
            str1 = strs[p + 1]
            str2 = strs[p + 2]
            i = 0
            j = 0

            while i < len(str1) and j < len(str2):
                a = str1[i]
                b = str2[j]
                if a == '\n':
                    break
                # 如果字符一样则++continue
                if a == b:
                    i = i + 1
                    j = j + 1
                    continue
                else:
                    # 如果不一样，先判断是不是我们要找的标志符号
                    if str1[i] in mark:
                        # 这里加一步i+1是为了判断--，……这样的两字符符号
                        if str1[i + 1] in mark:
                            i = i + 1
                        while i < len(str1):
                            if check_word(str1[i]) or str1[i] == '\n':
                                break
                            else:
                                i = i + 1
                        head = j
                        # 此时i在符号后的汉字上，取到下串再次与上串一致的位置，然后全部替换
                        while j < len(str2) and str1[i] != str2[j]:
                            j = j + 1
                        end = j
                        # 这里原来是用replace作的，就是第一次有用#4没用的那个，其实那个应该都没用，因为replace只替换第一个，没办法指定替换位置
                        # 于是后来换了思路，前后截断，重新拼接，这样就保证位置一定对
                        pre = str2[0:head]
                        suf = str2[end:]
                        # 替这里中间添加要替换的#4，#3，重新赋值回去
                        str3 = ''.join([pre, rep, suf])
                        str2 = str3
                        strs[p + 2] = str3
                        j = head
                    else:
                        while i < len(str1):
                            # 这里使用正则，如果上下不一致，且不是目标符号，则先找到上字符的下一个汉字在哪里
                            # 然后在下字符串中找，刚刚定位的汉字，这样重新是两个指针指向同一个汉字，继续执行代码
                            if check_word(str1[i]) or str1[i] == '\n':
                                break
                            else:
                                i = i + 1
                        while j < len(str2) and str1[i] != str2[j]:
                            j = j + 1
            with open(outf, 'w', encoding='UTF-8') as f2:
                f2.writelines(strs)


def check_word(str):
    # 正则方法，判断当前字符是不是汉字
    c = re.match('[\u4e00-\u9fa5]', str)
    return c


def com(fname):
    act(fname, ['—', '…', '：', '，', '；'], '#4 ', fname)
    act(fname, ['、'], '#3 ', fname)


if __name__ == '__main__':
    print(__file__)
    c = os.listdir()
    print(c)
    try:
        for i in range(len(c)):
            if c[i].endswith('mlf'):
                print(c[i])
                com(c[i])
        print('执行完毕，按任意键退出')
        s = raw_input()
    except Exception as e:
        print('some error accurs: ', e)
    # com('1.mlf')
