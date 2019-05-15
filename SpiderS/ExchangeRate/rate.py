import os
import time
from urllib.parse import unquote

import requests
from selenium.webdriver.support.select import Select
import xlrd
from click._compat import raw_input
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

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
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '',
}


def start_action():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    # page = webdriver.Chrome()  # 打开浏览器
    page = webdriver.Chrome(chrome_options=opts)  # 打开浏览器
    # page = webdriver.Chrome()  # 打开浏览器
    page.get('http://srh.bankofchina.com/search/whpj/search.jsp')

    select_usd = Select(page.find_element_by_xpath('//*[@id="pjname"]'))
    select_usd.select_by_visible_text('美元')

    btn = '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input'
    page.find_element_by_xpath(btn).click()

    selling_usd_rate_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[2]'
    selling_usd_rate = page.find_element_by_xpath(selling_usd_rate_position).text
    buying_usd_rate_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[4]'
    buying_usd_rate = page.find_element_by_xpath(buying_usd_rate_position).text
    timestamp_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[7]'
    timestamp = page.find_element_by_xpath(timestamp_position).text
    dicts = {'selling_usd_rate': selling_usd_rate, 'buying_usd_rate': buying_usd_rate, 'timestamp': timestamp}
    print(dicts)



if __name__ == '__main__':
    try:
        start_action()
    except Exception as e:
        print(e)
    # 根据id定位元素
    '''
 
    '''
