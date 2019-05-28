import requests

url = "http://192.168.3.153:8091/v1/handle_tx"
data = "data"
headers = {'Connection': 'Keep-Alive',
           'content-type': 'application/json; charset=utf-8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

resp = requests.post(url=url, data=data, headers=headers)
print(resp.text)
