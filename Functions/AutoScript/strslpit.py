str1 = 'No 87654321'
str2 = '开对日期: ”2012年09月18回'
str3 = '¥ 1153.85) ¥ 196.15\r\n\r\n(hs) ¥ 1350.00' + " "

criteria = '0123456789.'
tem1 = ''
for c in str1:
    if c in criteria:
        tem1 = tem1 + c
print(tem1)

tem2 = ''
for c in str2:
    if c in criteria:
        tem2 = tem2 + c
print(tem2)

tem3 = ''
arr = ['', '', '']
k = 0
for c in str3:
    if c in criteria:
        tem3 = tem3 + c
    elif c == ' ':
        if tem3 == '':
            continue
        else:
            arr[k] = tem3
            tem3 = ''
            k = k + 1
    else:
        continue

print(tem3)
print(arr)
print(str3)
