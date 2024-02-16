import numpy as np

from . import mysqlhandler as mysql


def calculate_ratio(current_date, conditions):
    """
    计算比率

    :param current_date: 日期
    :param conditions: sql
    :return: 元组(日期, 筛选后剩余数量, 总数)
    """
    if current_date.weekday() in [5, 6]:
        return str(current_date), None, None

    str_date = current_date.strftime('%Y%m%d')

    # 交易代码
    code = mysql.get_data_from_mysql(str_date, "代码")
    if code == -1:
        print(f"\n{current_date} 数据缺失")
        return str(current_date), None, None
    elif code:
        total = len(code)
        data_remain = mysql.get_data_from_mysql(str_date, "代码", conditions)
        remain = len(data_remain)
        return str(current_date), remain, total


def calculate_math(current_date, column, conditions, model='median'):
    """
    计算中位数

    :param current_date: 日期
    :param column: 需要计算中位数的列
    :param conditions: sql
    :param model: median,avg
    :return: 元组(日期, 中位数)
    """
    if current_date.weekday() in [5, 6]:
        return str(current_date), None

    str_date = current_date.strftime('%Y%m%d')

    # 交易代码
    code = mysql.get_data_from_mysql(str_date, "代码")
    if code == -1:
        print(f"\n{current_date} 数据缺失")
        return str(current_date), None
    elif code:
        data = mysql.get_data_from_mysql(str_date, column, conditions)
        # 判断数据是否为空
        if len(data) == 0:
            return str(current_date), '-'

        try:
            if model == 'median':
                return str(current_date), np.median(data)
            elif model == 'avg':
                return str(current_date), np.mean(data)
        except np.core._exceptions._UFuncNoLoopError as e:
            print('\n', e)
            print(data)
        except Exception as e:
            print('\n', '出现异常', e)
