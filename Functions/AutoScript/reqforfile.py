'''



function download(regno)//单一下载登记证明文件
{
	var form = document.getElementById("downloadform");
	form.action="/rs/conditionquery/byid.do?method=downloadregfile";
	form.submit();
}

function downloadattach(save_name,show_name)//下载附件
{
	var form = document.getElementById("downloadform");
	document.getElementById("save_name").value=save_name;
	document.getElementById("show_name").value=show_name;
	form.action="/rs/conditionquery/byid.do?method=downloadattach";
	form.submit();
}








https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadregfile


https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadattach

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: max-age=0
'Connection': 'keep-alive',
Content-Length: 133
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID=235473429.20480.0000; JSESSIONID=235473429.20480.0000; BIGipServerpool_zdw_www=+wr22ke2q2N+qql1wNGcmNIDgPeiHKk/D3OniUz6+Rhth8Ll1m3xu64oN9T49/h+yjpUcKwzfVpK/w==; RSOUT=qW2Dc4NcPz47JbGQJCZKncsHhy9P2yMdDjp4jsx9nFSnRh3hQJvD!2063536598; BIGipServerpool_rs=dHzTZk+QFoJktIdbgfFJe/GX0Jl48Auk/0yNPStZeae5kefdi78/yQfTyAAew1yq9g1ptko1SESyoCk=

Host: www.zhongdengwang.org.cn
Origin: https://www.zhongdengwang.org.cn
Referer: https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=viewfile&regno=03264760000393683312&type=1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
BIGipServerpool_zdw_www=OVFtlDb6+p8WKmdKei6fpzeg/uZ0PuruHJSeE7XMHjbuNeMLjSim4yhOwiPhmfFDYk6OTJpfLWynjw==; RSOUT=ypYsc4YhgpR8DvZHJvxSQphynm5JdCQKg8WVG2BFdGs05Kdfh4tm!2063536598; BIGipServerpool_rs=vO7vbAMLW1UJTE5Jk5VeP2241wWoXzno+QoX54tOhBcZZrM7lOKl4IECfwLa5TV33UeHadxgA47Jbsg=

JSESSIONID=235473429.20480.0000;
JSESSIONID=235473429.20480.0000
JSESSIONID=235473429.20480.0000
JSESSIONID=E9E60EF9115FAD0293FA84CB996873B4; BIGipServerpool_zdw_www=+wr22ke2q2N+qql1wNGcmNIDgPeiHKk/D3OniUz6+Rhth8Ll1m3xu64oN9T49/h+yjpUcKwzfVpK/w==; BIGipServerpool_rs=dHzTZk+QFoJktIdbgfFJe/GX0Jl48Auk/0yNPStZeae5kefdi78/yQfTyAAew1yq9g1ptko1SESyoCk=; RSOUT=rPnWc4YNWhQpJpf5hLJcL7QffPTSgZ22hspprxQG9LyHslngF5wP!2063536598
'''

import os
from urllib.parse import unquote

import requests
from click._compat import raw_input
from selenium import webdriver


def download_file(payload, dirpath):
    url = "https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadregfile"
    r = requests.post(url, data=payload, headers=headers)
    file = r.content
    with open(os.path.join(dirpath, (str(regno) + '.pdf')), 'wb') as f:  # 保存文件
        f.write(file)


def getattach_by_href(href):
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
    print(b)
    return a, b


def download_attach(pagea, position, payloada, dirpath):
    url = "https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadattach"
    href = pagea.find_element_by_xpath(('//*[@id="tab"]/tbody/tr[' + str(position) + ']/td[2]/a')).get_attribute('href')
    save_name, show_name = getattach_by_href(href)
    payloada['save_name'] = save_name
    payloada['show_name'] = show_name
    r = requests.post(url, data=payloada, headers=headers)
    file = r.content
    with open(os.path.join(dirpath, show_name), 'wb') as f:  # 保存文件
        f.write(file)
    # '//*[@id="tab"]/tbody/tr[3]/td[2]/a'
    # '//*[@id="tab"]/tbody/tr[4]/td[2]/a'


page = webdriver.Chrome()
page.get('https://www.zhongdengwang.org.cn/')
cs = page.get_cookies()
print(cs)

name = ''
pasw = ''
# 切换到frame
page.switch_to.frame(page.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/iframe"))
page.find_element_by_id('userCode').send_keys(name)
page.find_element_by_id('showpassword').click()
page.find_element_by_id('password').send_keys(pasw)
print('--请输入图片验证码： -------')
vali = raw_input()
print('您输入的验证码为： ' + vali)
page.find_element_by_id('validateCode').send_keys(vali)
page.find_element_by_id('login_btn').click()
page.switch_to.parent_frame()

cookie = '\''
for s in cs:
    cookie = cookie + s['name'] + '=' + s['value'] + '; '

cookie = cookie + '\''
print(cookie)
vali = raw_input()

# page.add_cookie({'name': 'JSESSIONID', 'value': '235473429.20480.0000', 'path': '/', 'secure': True})

print('go to view file')
page.get('https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=viewfile&regno=03291588000396823873&type=1')

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
    'Cookie': cookie,
}

regno = page.find_element_by_xpath('//*[@id="regno"]').get_attribute('value')
type = page.find_element_by_xpath('//*[@id="type"]').get_attribute('value')

payload = {'regno': regno,
           'type': type,
           'save_name': '',
           'show_name': '',
           }
urla = 'https://www.zhongdengwang.org.cn/rs/conditionquery/byid.do?method=downloadregfile'
r = requests.post(urla, data=payload, headers=headers)

print('sent post')
# 下载服务器download目录下的指定文件

file = r.content  # 获取文件内容
dirpath = r'c:\auto\down'

download_file(payload, dirpath)
download_attach(page, 3, payload, dirpath)
