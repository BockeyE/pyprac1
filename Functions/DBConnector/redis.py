import redis
conn = redis.Redis(host='127.0.0.1', port=6379)
# 可以使用url方式连接到数据库
# conn = Redis.from_url('redis://@localhost:6379/1')
conn.set('name', 'LinWOW')
print(conn.get('name'))
