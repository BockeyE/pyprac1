import copy
import time

import xlrd
from click._compat import raw_input
from selenium import webdriver
import sys

from selenium.webdriver.common.alert import Alert

com1 = ''
com2 = ''

page = webdriver.Chrome()  # 打开浏览器
page.get('https://www.zhongdengwang.org.cn/')
title = page.title  # 获得网页title
print('网页title： ' + title)
www = page.current_url  # 返回打开的网址
print('访问的地址： ' + www)

name = ''
pasw = ''

print('请在看到此提示后，在命令窗口正确输入验证码，并回车；输入失败时请重启程序')

# 切换到frame
page.switch_to.frame(page.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/iframe"))

while True:
    page.find_element_by_id('userCode').send_keys(name)
    page.find_element_by_id('showpassword').click()
    page.find_element_by_id('password').send_keys(pasw)
    print('请输入图片验证码： ')
    vali = raw_input()
    print('您输入的验证码为： ' + vali)
    page.find_element_by_id('validateCode').send_keys(vali)
    page.find_element_by_id('login_btn').click()
    time.sleep(0.2)
    try:
        check_info = page.find_element_by_xpath('//*[@id="con_one_1"]/div[3]').text
        print(check_info)
        if (not check_info) or check_info == '':
            break
        else:
            continue
    except Exception:
        break

# if not vali == 'go':
#     print('不执行脚本，即将退出')
#     exit()

# 最大化窗口
print('验证成功，继续执行')
page.maximize_window()

# 点击登陆按钮

# 跳出frame
page.switch_to.parent_frame()

# 点击按主体查询
page.find_element_by_xpath(
    "/html/body/div[2]/table[6]/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a").click()

# 点击 按投资金融入方查询
page.find_element_by_xpath(
    "/html/body/div[2]/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a").click()

# 填写各项出让人信息
# 填写 资金融入方名称
page.find_element_by_xpath('//*[@id="name"]').send_keys(com2)

print("资金融入方名称已经填写完毕，请按照下面的验证码图片，在命令行下方输入验证码，回车确定")
print("请输入验证码：")
vali2 = raw_input()
# 填写验证码
page.find_element_by_xpath('//*[@id="validateCode"]').send_keys(vali2)

# 点击，勾选 需要查询证明
page.find_element_by_xpath('//*[@id="confirm"]').click()
print('------验证正确，脚本继续执行---------------------------------')
# 点击，查询按钮
page.find_element_by_xpath('//*[@id="query"]').click()

# 点击 查看应收账款质押和转让登记
page.find_element_by_xpath('//*[@id="code"]/td[2]/a').click()

# 检查是否有记录

rec_count = page.find_element_by_xpath('//*[@id="detail_count"]').text
rec_count = int(rec_count)

if rec_count:
    print("查询结果已经显示，请按照下面的验证码图片，在命令行下方输入验证码，回车确定")
    print("请输入验证码：")
    vali3 = raw_input()
    # 输入验证码
    position = rec_count + 5
    page.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/input').send_keys(vali3)

    # 点击附件下载 链接
    page.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/span').click()

else:
    print("查询无结果，截图至目录")
    page.maximize_window()
    page.get_screenshot_as_file('C:\\auto\\pics\\' + com2 + '_查询结果.png')
