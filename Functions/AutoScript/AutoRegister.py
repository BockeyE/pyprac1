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
    print('读取的excel 页： ' + str(workbook.sheet_names()) + '。读取行数是： ' + str(row_num))
    sheet2_name = workbook.sheet_names()[0]
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    rows = target_sheet.row_values(row_num)  # 获取行内容
    return rows


# print(cols)


# ————————打开网页
from selenium.webdriver.support.select import Select

page = webdriver.Chrome()  # 打开浏览器
page.get('https://www.zhongdengwang.org.cn/')
title = page.title  # 获得网页title
print('网页title： ' + title)
www = page.current_url  # 返回打开的网址
print('访问的地址： ' + www)

name = ''
pasw = ''

print('请在看到此提示后，在命令窗口正确输入验证码，并回车；输入失败时请重启程序')

# 根据id定位元素
'''
 归档号      filling_number
登记期限    registration_period
出让人名称  transfer
组织机构代码/社会统一信用码   org_code
工商号/社会统一信用码 business_code
# 全球法人识别码  global_code
# 法人代表  representative
所属行业  sector
企业规模  scale
住所 ，中国 country
住所 省份 province
住所 城市 city
详细地址  address
转让合同号码      contract_no
合同币种          contract_currency
转让财产价值 元   total_assets 
转让财产描述      assets_description
'''
rows = readRow(1)
filling_number = rows[1]
registration_period = rows[11]
transfer = rows[0]
representative = rows[2]
org_code = rows[8]
sector = rows[3]
if not sector.endswith('业'):
    sector = sector + '业'
scale = rows[4]
country = '中国'
province = rows[5]
city = rows[6]
address = rows[7]
contract_no = rows[9]
contract_currency = '人民币'
total_assets = rows[10]
assets_description = rows[12]
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

# 最大化窗口
page.maximize_window()

# 点击登陆按钮

# 跳出frame
page.switch_to.parent_frame()

# 点击初始登记
page.find_element_by_xpath(
    "/html/body/div[2]/table[6]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a").click()

# 点击应收账款登记
page.find_element_by_xpath(
    "/html/body/div[2]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td").click()

# 是否已签合同，点击是
page.find_element_by_xpath('/html/body/div[2]/table[3]/tbody/tr[1]/td/input[1]').click()

# 点击下一步按钮
page.find_element_by_xpath('//*[@id="next"]').click()

# 获取选项列表
select = Select(page.find_element_by_xpath('//*[@id="timelimit"]'))
# 选择登记期限
select.select_by_visible_text(registration_period)

# 填写 填表人归档号
page.find_element_by_id("title").send_keys(filling_number)
time.sleep(1)
# 点击保存
page.find_element_by_xpath('/html/body/div[2]/form/div/input[1]').click()
time.sleep(1)
# 点击 增加出让人
page.find_element_by_xpath('//*[@id="addDebtor"]').click()

# 获取下拉列表
select = Select(page.find_element_by_xpath('//*[@id="debtorType"]'))
# 出让人类型选企业-2
select.select_by_index(2)

time.sleep(1)
# 填写各项出让人信息
# 出让人名称
page.find_element_by_xpath('//*[@id="debtorName"]').send_keys(transfer)

# 组织机构代码 / 社会统一信用码
page.find_element_by_xpath('//*[@id="orgCode"]').send_keys(org_code)

# 工商号 / 社会统一信用码
page.find_element_by_xpath('//*[@id="businessCode"]').send_keys(org_code)
# 全球法人识别码
# page.find_element_by_xpath('//*[@id="lei"]').send_keys('sada')
# 法人代表
page.find_element_by_xpath('//*[@id="responsiblePerson"]').send_keys(representative)
# select 所属行业
select2 = Select(page.find_element_by_xpath('//*[@id="industryCode"]'))
#
select2.select_by_visible_text(sector)
time.sleep(1)
# 企业规模
select3 = Select(page.find_element_by_xpath('//*[@id="scale"]'))
select3.select_by_visible_text(scale)

# 住所 ，中国
select4 = Select(page.find_element_by_xpath('//*[@id="country"]'))
select4.select_by_visible_text('中国')

# 住所 省份
select5 = Select(page.find_element_by_xpath('//*[@id="province"]'))
select5.select_by_visible_text(province)

# 住所 城市
select6 = Select(page.find_element_by_xpath('//*[@id="city"]'))
select6.select_by_visible_text(city)
# 详细地址
page.find_element_by_xpath('// *[ @ id = "address"]').send_keys(address)
time.sleep(1)
# 点击保存按钮
page.find_element_by_xpath('//*[@id="saveButton"]').click()

# 增加受让人信息
page.find_element_by_xpath('//*[@id="secondName"]').click()

# 增加填表人 为受让人
page.find_element_by_xpath('//*[@id="addDebtorAuto"]').click()
time.sleep(1)
# 跳转到转让财产信息
page.find_element_by_xpath('//*[@id="typeName"]').click()
# 转让合同号码
page.find_element_by_xpath('//*[@id="maincontractno"]').send_keys(contract_no)

# 合同币种 select
select7 = Select(page.find_element_by_xpath('//*[@id="maincontractcurrency"]'))
select7.select_by_visible_text(contract_currency)
# 转让财产价值 元 inpu
page.find_element_by_xpath('//*[@id="maincontractsum"]').send_keys(str(total_assets))
# 转让财产描述 textarea
page.find_element_by_xpath('//*[@id="description"]').send_keys(assets_description)
time.sleep(1)
page.get_screenshot_as_file('C:\\auto\\pics\\' + filling_number + '.png')
time.sleep(1)
# 点击这里上传附件
# page.find_element_by_xpath('//*[@id="attachinfo"]').click()
# 点击保存按钮
# page.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/table[2]/tbody/tr/td/input').click()
# 点击预览按钮
# page.find_element_by_xpath('//*[@id="previewbutton"]').click()

# #点击返回主页按钮
# page.find_element_by_xpath('//*[@id="previewbutton"]').click()

# #点击alert确认
# Alert(page).accept();

# b.close()  # 关闭当前窗口
# b.quit()  # 关闭浏览器
