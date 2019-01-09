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


def readRow(row_num):
    workbook = xlrd.open_workbook(r'C:\auto\AutoFill.xlsx')
    print('读取的excel 页： ' + workbook.sheet_names())
    sheet2_name = workbook.sheet_names()[0]
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    rows = target_sheet.row_values(row_num)  # 获取行内容
    return rows


# print(cols)


# ————————打开网页
from selenium.webdriver.support.select import Select

page = webdriver.Chrome()  # 打开浏览器
page.get('https://inv-veri.chinatax.gov.cn')
title = page.title  # 获得网页title
print('网页title： ' + title)
www = page.current_url  # 返回打开的网址
print('访问的地址： ' + www)

print('请在看到此提示后，在命令窗口正确输入验证码，并回车；输入失败后请重启程序')

# 根据id定位元素

fpdm = '3700174130'
fphm = '18806918'
kprq = '20181106'
kjje = '944569.83'

# 切换到frame

page.find_element_by_id('fpdm').send_keys(fpdm)
page.find_element_by_id('fphm').send_keys(fphm)
page.find_element_by_id('kprq').send_keys(kprq)
page.find_element_by_id('kjje').send_keys(kjje)
# page.find_element_by_id('yzm_img').click()
# if Alert(page):
#     Alert(page).accept()

print('请输入图片验证码： ')
vali = raw_input()
print(vali)

page.find_element_by_id('yzm').send_keys(vali)
time.sleep(1)
page.maximize_window()
page.find_element_by_id('checkfp').click()
time.sleep(1)
# if not vali == 'go':
#     print('不执行脚本，即将退出')
#     exit()
page.get_screenshot_as_file('C:\\auto\\pics\\发票代码' + fpdm + '.png')
# 最大化窗口
# page.maximize_window()
