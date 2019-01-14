import os
import time
from urllib.parse import unquote
import requests
import xlrd
from click._compat import raw_input
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import threading

mkpath = "c:\\auto\\down\\"

headers = {
    'Connection': 'keep-alive',
    'Content-Length': '133',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://www.zhongdengwang.org.cn',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.zhongdengwang.org.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=viewfile&regno=03291588000396823873&type=1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '',
}


def circle_download(page, p, target):
    filelatter = page.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(p + 3) + ']/td[6]').text
    page.find_element_by_xpath(
        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(p + 3) + ']/td[7]/span').click()
    # 获取当前列是主要 机构名
    page.switch_to_window(page.window_handles[1])
    time.sleep(0.5)
    regno = page.find_element_by_xpath('//*[@id="regno"]').get_attribute('value')
    type = page.find_element_by_xpath('//*[@id="type"]').get_attribute('value')
    subdir = mkdir(os.path.join(mkpath, target, target + "_" + filelatter))
    # 机构名与主体名拼接成新名称
    payload = {'regno': regno,
               'type': type,
               'save_name': '',
               'show_name': '',
               }
    attach_limit = 0
    while True:
        try:
            page.find_element_by_xpath('//*[@id="tab"]/tbody/tr[' + str(2 + attach_limit) + ']/td[2]/a')
            attach_limit += 1
        except Exception:
            break
        # //*[@id="tab"]/tbody/tr[3]/td[2]/a   第一个附件
    download_pdf(payload, subdir, regno)
    if attach_limit:
        for i in range(1, attach_limit):
            download_attach(page, i, payload, subdir)

    page.close()
    page.switch_to_window(page.window_handles[0])


def download_pdf(payload, dirpath, regno):
    url = "https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadregfile"
    r = requests.post(url, data=payload, headers=headers)
    file = r.content
    with open(os.path.join(dirpath, (str(regno) + '.pdf')), 'wb') as f:  # 保存文件
        f.write(file)


def get_attach_by_href(href):
    cre = '()'
    aim = ''
    flag1 = False
    for c in href:
        if c == cre[0]:
            flag1 = True
            continue
        if c == cre[1]:
            flag1 = False
        if flag1:
            aim = aim + c
    a, b = aim.split(',')
    a = a.split('\'')[1]
    b = b.split('\'')[1]
    b = unquote(b, 'utf-8')
    return a, b


def download_attach(page, index, payload, dirpath):
    url = "https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadattach"
    href = page.find_element_by_xpath(('//*[@id="tab"]/tbody/tr[' + str(index + 2) + ']/td[2]/a')).get_attribute('href')
    save_name, show_name = get_attach_by_href(href)
    payload['save_name'] = save_name
    payload['show_name'] = show_name
    r = requests.post(url, data=payload, headers=headers)
    file = r.content
    with open(os.path.join(dirpath, show_name), 'wb') as f:  # 保存文件
        f.write(file)
    # '//*[@id="tab"]/tbody/tr[3]/td[2]/a'  第一个附件
    # '//*[@id="tab"]/tbody/tr[4]/td[2]/a'


def mkdir(path):
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        pass
    return path


def getlines():
    workbook = xlrd.open_workbook(r'C:\auto\search_company.xlsx')
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    return target_sheet.nrows


def zip_count(dirpath):
    files = os.listdir(dirpath)
    count = 0
    for f in files:
        if f.endswith("zip"):
            count += 1
    return count


def zip_listen(dirpath, newname):
    cou1 = zip_count(dirpath)
    while True:
        time.sleep(1)
        cou2 = zip_count(dirpath)
        if cou1 == cou2:
            continue
        else:
            break
    rename_latest_zip(dirpath, newname)
    print('后台下载： ' + newname + ' 已经完成')
    return


def rename_latest_zip(dirpath, newname):
    try:
        files = os.listdir(dirpath)
        wholefiles = []
        for f in files:
            f = dirpath + f
            if f.endswith('zip'):
                wholefiles.append(f)
        tem = max(wholefiles, key=os.path.getctime)
        os.rename(os.path.join(tem), os.path.join(dirpath, newname) + ".zip")
    except Exception:
        print("-------文件已经存在，请注意移走已有文件。错误目标： " + newname + "------")


def readRow(row_num):
    workbook = xlrd.open_workbook(r'C:\auto\search_company.xlsx')
    print('读取的excel 页： ' + str(workbook.sheet_names()) + '。读取行数是： ' + str(row_num))
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # 获取整行和整列的值（数组）
    rows = target_sheet.row_values(row_num)  # 获取行内容
    return rows


def start_action():
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
    cs = page.get_cookies()
    cookie = '\''
    for s in cs:
        cookie = cookie + s['name'] + '=' + s['value'] + '; '
    cookie = cookie + '\''
    headers['Cookie'] = cookie

    # 循环保证验证通过
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
    for i in range(1, lines):
        rows = readRow(i)
        target_com = rows[0]
        print("")
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
        print("资金融入方名称已经填写，请输入验证码，回车确定：")
        # 循环保证验证通过
        while True:
            vali2 = raw_input()
            # 填写验证码
            page.find_element_by_xpath('//*[@id="validateCode"]').send_keys(vali2)
            page.find_element_by_xpath('//*[@id="confirm"]').click()
            time.sleep(0.1)
            try:
                res1 = page.find_element_by_xpath('//*[@id="code"]').text
                if res1 == '校验码错误':
                    print("验证码有误，请重输入：")
                    continue
                else:
                    break
            except Exception:
                break
        # 点击，勾选 需要查询证明
        print('------验证正确，脚本继续执行---------------------------------')
        # 点击，查询按钮
        page.find_element_by_xpath('//*[@id="query"]').click()
        # 点击 查看应收账款质押和转让登记
        page.find_element_by_xpath('//*[@id="code"]/td[2]/a').click()
        # 检查是否有记录
        rec_count = page.find_element_by_xpath('//*[@id="detail_count"]').text
        rec_count = int(rec_count)
        # 大于100 时，进入方法，逐个下载
        if rec_count > 100:
            print("查询结果已经显示，记录数超过100，开始逐个下载")
            for k in range(1, rec_count):
                m = k % 10
                if m:
                    circle_download(page, m, target_com)
                    curen = page.find_element_by_xpath(
                        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(m + 3) + ']/td[6]').text
                    print('完成第 ' + str(k) + ' 条  ： ' + curen)
                else:
                    circle_download(page, 10, target_com)
                    page.find_element_by_xpath(
                        '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[14]/td/div/a[3]').click()
                    print('已经完成10个条目，翻页继续')
            print("该名称下的文件已经下载完毕，请输入任意命令，继续执行文档中未执行的查询")
            vali6 = raw_input()
            # 返回主页
            page.find_element_by_xpath('//*[@id="dc"]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/input').click()
            continue
        elif 10 <= rec_count <= 100:
            rec_count = 10
        if rec_count >= 100:
            pass
        elif rec_count:
            print("查询结果已经显示，请在命令行下方输入验证码，回车即开始打包下载")
            print("请输入验证码：")
            position = rec_count + 5
            while True:
                vali3 = raw_input()
                page.find_element_by_xpath(
                    '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/input').send_keys(
                    vali3)
                # 点击附件下载 链接
                page.find_element_by_xpath(
                    '//*[@id="dc"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(position) + ']/td/span').click()
                try:
                    Alert(page).accept()
                    print('验证码有误，请重试')
                except Exception:
                    break
            print('验证通过')
            t = threading.Thread(target=zip_listen, args=(mkpath, target_com))
            t.start()
            print('开始后台下载，如果中断程序文件仍会下载，但会失去重命名')
        else:
            print("查询无结果，截图至目录 c:/auto/pics ")
            page.maximize_window()
            page.get_screenshot_as_file('C:\\auto\\pics\\' + target_com + '_查询结果.png')

        print("请在键盘输入任意字符，继续执行excel中待查的查询")
        print()
        vali4 = raw_input()
        # 返回主页
        page.find_element_by_xpath('//*[@id="dc"]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/input').click()

    print("表格中的数据已经查询完毕，退出程序")


if __name__ == '__main__':
    start_action()
