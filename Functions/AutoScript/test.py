import copy
import time

import xlrd
from click._compat import raw_input
from selenium import webdriver
import sys

# import os, sys
# base_dir = os.path.dirname(__file__)
# sys.path.append(base_dir)
from selenium.webdriver.common.alert import Alert

# ————————打开网页
from selenium.webdriver.support.select import Select

page = webdriver.Chrome()  # 打开浏览器
page.get('https://www.zhongdengwang.org.cn/')
title = page.title  # 获得网页title
print(title)
www = page.current_url  # 返回打开的网址
print(www)

name = ''
pasw = ''

# 切换到frame
page.switch_to.frame(page.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/iframe"))

page.find_element_by_id('userCode').send_keys(name)
page.find_element_by_id('showpassword').click()
page.find_element_by_id('password').send_keys(pasw)
page.find_element_by_id('imgId').screenshot('C:\\auto\\valiCache\\tem.png')

vali = raw_input()
print(vali)

page.find_element_by_id('validateCode').send_keys(vali)
# if not vali == 'go':
#     print('不执行脚本，即将退出')
#     exit()

# 最大化窗口
page.maximize_window()

# 点击登陆按钮
page.find_element_by_id('login_btn').click()
# 跳出frame
page.switch_to.parent_frame()
