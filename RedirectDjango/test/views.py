# -*- coding: UTF-8 -*-
import requests
from django.http import HttpResponse

status_code = 200
err_code = 500


# 测试接口
# http://127.0.0.1:9090/v2/test?utype=get&url=http://www.baidu.com
def test(request, format=None):
    utype = request.GET['utype']
    url = request.GET['url']
    print('==============>test')
    if utype == 'get':
        ret = requests.get(url, None)
    if utype == 'post':
        ret = requests.get(url, None)
    print(type(ret))
    return HttpResponse(content=ret.content,
                        status=ret.status_code,
                        content_type=ret.headers['Content-Type'])
