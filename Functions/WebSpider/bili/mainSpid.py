import requests
import json
import random
import pymongo
import sys
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool


def datetime_to_timestamp_in_millis(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()


reload(sys)


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents('user.txt')
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
# Please replace your own proxies.
proxies = {
    'http': 'http://120.26.110.59:8080',
    'http': 'http://120.52.32.46:80',
    'http': 'http://218.85.133.62:80',
}
time1 = time.time()

urls = []

for m in range(5214, 5215):

    for i in range(m * 100, (m + 1) * 100):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)


    def getsource(url):
        payload = {
            '_': datetime_to_timestamp_in_millis(datetime.datetime.now()),
            'mid': url.replace('https://space.bilibili.com/', '')
        }
        jscontent = requests \
            .session() \
            .post('http://space.bilibili.com/ajax/member/GetInfo',
                  headers=head,
                  data=payload,
                  proxies=proxies).text
        time2 = time.time()

        jsdict = json.loads(jscontent)
        statusjson = jsdict['status'] if 'status' in jsdict.keys() else False
        if statusjson:
            if 'data' in jsdict.keys():
                jsData = jsdict['data']
                mid = jsData['mid']
                name = jsData['name']
                sex = jsData['sex']
                rank = jsData['rank']
                face = jsData['face']
                regtimestamp = jsData['regtime']
                regtime_local = time.localtime(regtimestamp)
                regtime = time.strftime('%Y-%m-%d %H:%M:%S', regtime_local)
                spacesta = jsData['spacesta']
                birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                sign = jsData['sign']
                sign = jsData['sign']
                level = jsData['level_info']['current_level']
                OfficialVerifyType = jsData['official_verify']['type']
                OfficialVerifyDesc = jsData['official_verify']['desc']
                vipType = jsData['vip']['vipType']
                vipStatus = jsData['vip']['vipStatus']
                toutu = jsData['toutu']
                toutuId = jsData['toutuId']
                coins = jsData['coins']
                print("Succeed get user info: " + str(mid) + "\t" + str(time2 - time1))
                try:
                    res = requests.get(
                        'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp').text
                    viewinfo = requests.get(
                        'https://api.bilibili.com/x/space/upstat?mid=' + str(mid) + '&jsonp=jsonp').text
                    js_fans_data = json.loads(res)
                    js_viewdata = json.loads(viewinfo)
                    following = js_fans_data['data']['following']
                    fans = js_fans_data['data']['follower']
                    archiveview = js_viewdata['data']['archive']['view']
                    article = js_viewdata['data']['article']['view']
                except:
                    following = 0
                    fans = 0
                    archiveview = 0
                    article = 0

if __name__ == "__main__":
    pool = ThreadPool(1)
    try:
        results = pool.map(getsource, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()
