from . import mysqlhandler as mysql


def calculate_ratio(current_date, data_consider):
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
