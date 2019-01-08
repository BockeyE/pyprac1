# 导入cv模块
import cv2 as cv

# 读取图像，支持 bmp、jpg、png、tiff 等常用格式
import pytesseract

img = cv.imread("c:\\auto\\valiCache\\fap.png")
# 创建窗口并显示图像
size = img.shape
print(size)
height = size[0]
width = size[1]
print(height)
print(width)

# [height,width]
fpdm_img = img[0:(height // 6), 0:(width // 3)]
fphm_img = img[0:(height // 6), ((width * 2) // 3):((width * 79) // 90)]
kprq_img = img[((height * 9) // 60):((height * 12) // 60), ((width * 2) // 3):width]
je_img = img[((height * 37) // 60):((height * 45) // 60), ((width * 20) // 30):((width * 115) // 120)]

code1 = pytesseract.image_to_string(fpdm_img)
print('read pic1')
print(code1)
code2 = pytesseract.image_to_string(fphm_img)
print('read pic2')
print(code2)
code3 = pytesseract.image_to_string(kprq_img, lang='chi_sim')
print('read pic3')
print(code3)
code4 = pytesseract.image_to_string(je_img) + " "
print('read pic4')
print(code4)

criteria = '0123456789.'
tem2 = ''
for c in code2:
    if c in criteria:
        tem2 = tem2 + c
print(tem2)

tem3 = ''
for c in code3:
    if c in criteria:
        tem3 = tem3 + c
print(tem3)

tem4 = ''
arr = ['', '', '']
k = 0
for c in code4:
    if c in criteria:
        tem4 = tem4 + c
    elif c == ' ':
        if tem4 == '':
            continue
        else:
            arr[k] = tem4
            tem4 = ''
            k = k + 1
    else:
        continue

print(arr)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# ret, res = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)
cv.namedWindow("Image")
cv.imshow("Image", je_img)
cv.waitKey(0)
# 释放窗口
cv.destroyAllWindows()
