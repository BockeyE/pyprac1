import copy
import os
import time

import xlrd
from click._compat import raw_input
from selenium import webdriver
import sys

from selenium.webdriver.common.alert import Alert


def mkdir(path):
    import os
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


# 定义要创建的目录
mkpath = "c:\\auto\\down\\"
# 调用函数
mkdir(mkpath)


def pdf_count(mkpath):
    files = os.listdir(mkpath)
    count = 0
    for f in files:
        if f.endswith("pdf"):
            count += 1
    return count


def rename_latest(uppath, newname, k):
    try:
        files = os.listdir(uppath)
        wholefiles = []
        for f in files:
            f = uppath + f
            wholefiles.append(f)
        tem = max(wholefiles, key=os.path.getctime)
        os.rename(os.path.join(tem), os.path.join(uppath, newname) + ".pdf")
    except Exception:
        print("-------文件已经存在，请注意移走已经查询过的文件，下载继续执行。错误文件： NO." + str(k) + "------")


def circle_download(page1, p, target_com, k):
    count1 = pdf_count(mkpath)
    page1.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(p + 3) + ']/td[7]/span').click()
    # //*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[7]/span
    # 获取当前列是主要 机构名
    filelatter = page1.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(p + 3) + ']/td[6]').text
    page1.switch_to_window(page.window_handles[1])
    page1.find_element_by_xpath('//*[@id="tab"]/tbody/tr[2]/td[2]/a').click()
    count2 = pdf_count(mkpath)
    while 1:
        if count2 == count1:
            time.sleep(0.1)
            count2 = pdf_count(mkpath)
            continue
        else:
            break
    # 机构名与主体名拼接成新文件名称
    rename_latest(mkpath, target_com + "_" + filelatter + "_NO." + str(k), k)
    page1.close()
    page1.switch_to_window(page.window_handles[0])


def getlines():
    workbook = xlrd.open_workbook(r'C:\auto\search_company.xlsx')
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    return target_sheet.nrows


def readRow(row_num):
    workbook = xlrd.open_workbook(r'C:\auto\search_company.xlsx')
    print('读取的excel 页： ' + str(workbook.sheet_names()) + '。读取行数是： ' + str(row_num))
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    rows = target_sheet.row_values(row_num)  # 获取行内容
    return rows


opts = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 2, 'download.default_directory': mkpath}
opts.add_experimental_option('prefs', prefs)

page = webdriver.Chrome(chrome_options=opts)  # 打开浏览器
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
    print('--请输入图片验证码： -------')
    vali = raw_input()
    print('您输入的验证码为： ' + vali)
    page.find_element_by_id('validateCode').send_keys(vali)
    page.find_element_by_id('login_btn').click()
    time.sleep(0.5)
    try:
        check_info = page.find_element_by_xpath('//*[@id="con_one_1"]/div[3]').text
        print(check_info)
        if (not check_info) or check_info == '':
            break
        else:
            continue
    except Exception:
        break

# 最大化窗口
print('验证成功，继续执行')
page.maximize_window()

# 点击登陆按钮

# 跳出frame

page.switch_to.parent_frame()

lines = getlines()

for i in range(lines - 1):
    rows = readRow(i + 1)
    target_com = rows[0]
    print('--------正在查询的目标是： ' + target_com + ' ---------')
    # 点击按主体查询
    page.find_element_by_xpath(
        "/html/body/div[2]/table[6]/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a").click()

    # 点击 按投资金融入方查询
    page.find_element_by_xpath(
        "/html/body/div[2]/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a").click()

    # 填写各项出让人信息
    # 填写 资金融入方名称
    page.find_element_by_xpath('//*[@id="name"]').send_keys(target_com)

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

    if rec_count > 100:
        print("查询结果已经显示，记录数超过100，开始逐个下载")
        for k in range(8, 12):
            m = k % 10
            if m:
                circle_download(page, m, target_com, k)
            else:
                circle_download(page, 10, target_com, k)
                page.find_element_by_xpath('//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[14]/td/div/a[3]').click()
        print("该名称下的文件已经下载完毕，请输入任意命令，继续执行文档中未执行的查询")
        vali2 = raw_input()
        # 返回主页
        page.find_element_by_xpath('//*[@id="dc"]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/input').click()
        continue
    elif 10 <= rec_count <= 100:
        rec_count = 10
    elif rec_count:

        print("查询结果已经显示，请在命令行下方输入验证码，回车即开始打包下载")
        print("请输入验证码：")
        vali3 = raw_input()
        # 输入验证码
        position = rec_count + 5
        print('position' + str(position))
        page.find_element_by_xpath(
            '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/input').send_keys(vali3)

        # 点击附件下载 链接
        page.find_element_by_xpath(
            '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/span').click()

    else:
        print("查询无结果，截图至目录 c:/auto/pics，")
        page.maximize_window()
        page.get_screenshot_as_file('C:\\auto\\pics\\' + target_com + '_查询结果.png')

    print("请在键盘输入任意字符，继续执行excel中待查的查询")
    vali2 = raw_input()
    # 返回主页
    page.find_element_by_xpath('//*[@id="dc"]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/input').click()

print("表格中的数据已经查询完毕，退出程序")
