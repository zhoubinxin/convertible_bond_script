import mysql.connector


def get_data_from_mysql(table, column, conditions=None, database='convertible_bond'):
    """
    从MySQL数据库中获取数据

    :param table: 数据表
    :param column: 列
    :param conditions: 条件，默认为None
    :param database: 数据库名，默认为convertible_bond
    :return: 查询到的数据，如果数据表不存在则返回-1
    """
    # 构建查询语句
    if conditions is None:
        conditions = []
    query = f"SELECT `{column}` FROM `{table}`"

    conditions.append(f"`{column}` is not null")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # print(query)

    # 使用上下文管理器处理数据库连接和游标
    with mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database=database
    ) as connection:
        if not check_table_exists(connection, table):
            return -1

        with connection.cursor() as cursor:
            # 执行查询语句
            cursor.execute(query)
            results = cursor.fetchall()
            data = [row[0] for row in results]

    return data


def check_table_exists(connection, table):
    """
    检查数据表是否存在

    :param connection: 数据库连接
    :param table: 数据表
    :return: 数据表存在返回True，否则返回False
    """
    query = f"SHOW TABLES LIKE '{table}'"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result is not None


def is_complete(current_date):
    """
    检查数据表是否完整

    :return: 返回不完整的数据表
    """
    # 筛选条件
    conditions = [
        "代码 is NULL or 代码 == '--'",
    ]

    code = get_data_from_mysql(current_date, "代码", conditions)
    if code != -1 and len(code) > 0:
        print(f"{current_date} 数据表不完整")
        return str(current_date), len(code)
