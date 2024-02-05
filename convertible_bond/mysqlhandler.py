import mysql.connector
from interval import Interval


def get_data_from_mysql(table, column, condition=None):
    # 建立数据库连接
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='convertible_bond'
    )

    if not check_table_exists(connection, table):
        return -1

    # 创建游标
    cursor = connection.cursor()

    # 构建查询语句
    query = f"SELECT `{column}` FROM `{table}`"
    where_clause = []

    # 添加过滤条件
    if condition:
        if condition["consider_cv"]:
            where_clause.append(f"`转股价格` BETWEEN {condition['cv_range']}")
        if condition["consider_ytm"]:
            where_clause.append(condition['ytm_range'])

    if where_clause:
        query += " WHERE " + " AND ".join(where_clause)

    # print(query)
    # 执行查询语句
    cursor.execute(query)

    # 获取查询结果
    results = cursor.fetchall()

    # 将查询结果转换为列表
    data = [row[0] for row in results]

    # 关闭游标对象和连接对象
    cursor.close()
    connection.close()

    return data


def check_table_exists(connection, table):
    cursor = connection.cursor()
    query = f"SHOW TABLES LIKE '{table}'"
    # print(query)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    return result is not None
