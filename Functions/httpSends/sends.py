import requests

url = "http://59.110.141.70:9091/server/apis/sigNature"
# data = '{"systemId": "system1", "priKey": "8d7afe7f6438c65e02c0942950832e3920ec76dc44d0843848622b82419c8882"}'
data = '{}'
# 字符串格式
res = requests.post(url=url, data=data)
print(res.text)
