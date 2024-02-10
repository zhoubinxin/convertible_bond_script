import mysql.connector


def get_data_from_mysql(table, column, conditions=None):
    """
    从MySQL数据库中获取数据

    :param table: 数据表
    :param column: 列
    :param conditions: 条件，默认为None
    :return: 查询到的数据，如果数据表不存在则返回-1
    """
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

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

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
    """
    检查数据表是否存在

    :param connection: 数据库连接
    :param table: 数据表
    :return: 数据表存在返回True，否则返回False
    """
    cursor = connection.cursor()
    query = f"SHOW TABLES LIKE '{table}'"
    # print(query)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    return result is not None
