import redis
from redis import Redis

conn = Redis(host='59.110.141.70', port=16379)
# 可以使用url方式连接到数据库
# conn = Redis.from_url('redis://@localhost:6379/1')
conn.set('name', 'LinWOW')
print(conn.get('name'))
