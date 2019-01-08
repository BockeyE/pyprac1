# 再次读取识别验证码
import cv2
import pytesseract
from PIL import Image

vali1 = "c:\\auto\\valiCache\\tem1.png"
vali2 = "c:\\auto\\valiCache\\tem2.png"
vali3 = "c:\\auto\\valiCache\\tem3.png"
vali4 = "c:\\auto\\valiCache\\tem4.png"
vali5 = "c:\\auto\\valiCache\\tem5.png"
print('read file')
import os

# print(os.path.getsize(vali))

print('====')
img = cv2.imread(vali1)
# 灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img1 = Image.open(vali1)
code1 = pytesseract.image_to_string(gray)
print('read pic1')
print(code1)
img2 = Image.open(vali2)
code2 = pytesseract.image_to_string(img2)
print('read pic2')
print(code2)
img3 = Image.open(vali3)
code3 = pytesseract.image_to_string(img3)
print('read pic3')
print(code3)
img4 = Image.open(vali4)
code4 = pytesseract.image_to_string(img4)
print('read pic4')
print(code4)
img5 = Image.open(vali5)
code5 = pytesseract.image_to_string(img5)
print('read pic5')
print(code5)
# # 识别出来验证码去特殊符号，用到了正则表达式，这是我第一次用，之前也没研究过，所以用的可能粗糙，请见谅
# b = ''
# for i in code.strip():
#     pattern = re.compile(r'[a-zA-Z0-9]')
#     m = pattern.search(i)
#     if m != None:
#         b += i
# # 输出去特殊符号以后的验证码
# print(b)
# # 把b的值输入验证码输入框
# driver.find_element_by_name("verificationCode").send_keys(b)
#    # 点击登录按钮
# driver.find_element_by_class_name('login-form-btn-submit').click()
#    # 定时等待5秒，如果验证码识别错误，提示验证码错误需要等一会儿才能继续操作
# time.sleep(5)
#    # 获取cookie，并把cookie转化为字符串格式
# cookie1 = str(driver.get_cookies())
# print(cookie1)
# # 第二次用正则表达式，同样有点粗糙，代码实现的功能就是看cookie里是否有tokenId这个词，如果有说明登录成功，跳出循环，可以进行后面的自动化操作，如果没有，则表示登录失败，继续识别验证码
# matchObj = re.search(r'tokenId', cookie1, re.M | re.I)
# if matchObj:
#     print(matchObj.group())
#     break
# else:
#     print("No match!!")
