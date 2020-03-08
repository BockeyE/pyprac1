import pymysql

# 创建一个连接对象，再使用创建游标
con = pymysql.connect(host='127.0.0.1', port=3306, user='aaa', passwd='123456', db='infoweb')
cursor = con.cursor()

# 执行一个SQL语句
sql = "select * from user"
cursor.execute(sql)

# 从游标中取出所有记录放到一个序列中并关闭游标
result = cursor.fetchall()
print(result)
cursor.close()