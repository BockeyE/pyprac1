import redis
from redis import Redis

conn = Redis(host='47.100.39.147', port=6379)
# 可以使用url方式连接到数据库
# conn = Redis.from_url('redis://@localhost:6379/1')
conn.set('name', 'lily')
print(conn.get('name'))
