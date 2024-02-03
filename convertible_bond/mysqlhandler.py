import mysql.connector

# 建立数据库连接
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='convertible_bond'
)

# 创建游标
cursor = connection.cursor()

# 执行查询
cursor.execute("SELECT * FROM `20240202`")

# 获取查询结果
results = cursor.fetchall()

# 打印查询结果
for result in results:
    print(result)

# 关闭游标和数据库连接
cursor.close()
connection.close()
