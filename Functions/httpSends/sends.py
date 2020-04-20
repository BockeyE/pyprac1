import requests

# url = "http://59.110.141.70:9091/server/apis/sigNature"
url = "http://47.93.18.100:9015/phone/case/findById?caseId=9ca3097f1fcb429cbb74b098d8502e8c"
# data = '{"systemId": "system1", "priKey": "8d7afe7f6438c65e02c0942950832e3920ec76dc44d0843848622b82419c8882"}'
data = '{}'
head = {'Content-Type': 'application/json', 'api-version': '1.0.0'
    , 'Referer': 'http://localhost:8765/',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    , 'Accept': '*', 'Access-Control-Allow-Credentials': 'true'
        }
# 字符串格式
res = requests.post(url=url, headers=head, data=data)
print(res.text)
