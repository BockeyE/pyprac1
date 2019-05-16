from selenium.webdriver.support.select import Select
from selenium import webdriver


def start_action():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    page = webdriver.Chrome(chrome_options=opts)  # 打开浏览器
    page.get('http://srh.bankofchina.com/search/whpj/search.jsp')

    select_usd = Select(page.find_element_by_xpath('//*[@id="pjname"]'))
    select_usd.select_by_visible_text('美元')

    btn = '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input'
    page.find_element_by_xpath(btn).click()
    # 现汇买入价，最新，也就是用户的美元-->人民币时参考的汇率
    selling_usd_rate_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[2]'
    selling_usd_rate = page.find_element_by_xpath(selling_usd_rate_position).text
    # 现汇卖出价，最新，也就是用户的人民币-->美元时参考的汇率
    buying_usd_rate_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[4]'
    buying_usd_rate = page.find_element_by_xpath(buying_usd_rate_position).text
    # 时间戳
    timestamp_position = '/html/body/div/div[4]/table/tbody/tr[2]/td[7]'
    timestamp = page.find_element_by_xpath(timestamp_position).text
    dicts = {'user_selling_usd_rate': selling_usd_rate, 'user_buying_usd_rate': buying_usd_rate, 'timestamp': timestamp}
    print(dicts)


if __name__ == '__main__':
    try:
        start_action()
    except Exception as e:
        print(e)
