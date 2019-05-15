import requests

url = "http://192.168.3.153:8091/v1/handle_tx"
data = "data"
# headers = {'content-type': 'application/json; charset=utf-8'}
headers = None
resp = requests.post(url=url, data=data, headers=headers)
print(resp.text)
