# 再次读取识别验证码
import cv2
import pytesseract
from PIL import Image

pic = "c:\\auto\\valiCache\\fap.png"

print('read file')
import os

# print(os.path.getsize(vali))

print('====')
img = cv2.imread(pic)
# 灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img1 = Image.open(pic)
code1 = pytesseract.image_to_string(gray)
print('read pic1')
print(code1)

# # 识别出来验证码去特殊符号，用到了正则表达式，这是我第一次用，之前也没研究过，所以用的可能粗糙，请见谅
# b = ''
# for i in code.strip():
#     pattern = re.compile(r'[a-zA-Z0-9]')
#     m = pattern.search(i)
#     if m != None:
#         b += i
