from . import mysqlhandler as mysql


def calculate_ratio(current_date, data_consider):
    """
    计算比率

    :param current_date: 日期
    :param data_consider: sql
    :return: 元组(日期, 筛选后剩余数量, 总数)
    """
    if current_date.weekday() in [5, 6]:
        return str(current_date), None, None

    total = None
    remain = None

    str_date = current_date.strftime('%Y%m%d')

    # 交易代码
    code = mysql.get_data_from_mysql(str_date, "代码")
    if code == -1:
        print(f"\n{current_date} 数据缺失")
        return str(current_date), remain, total
    elif code:
        total = len(code)
        data_remain = mysql.get_data_from_mysql(str_date, "代码", data_consider)
        remain = len(data_remain)
        return str(current_date), remain, total
