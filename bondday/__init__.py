import numpy as np

from . import api
from .bonddb import BondDB


class BondDay(object):
    @classmethod
    def db_init(cls):
        """
        初始化数据库

        :return:
        """
        print('初始化数据库中...')
        BondDB.init()
        print('初始化完成')
        cls.db_init_executed = True

    @classmethod
    def ratio(cls, current_date, conditions):
        """
        计算比率

        :param current_date: 日期
        :param conditions: sql
        :return: 元组(日期, 筛选后剩余数量, 总数)
        """
        bond_day = current_date.strftime('%Y-%m-%d')
        if not api.is_trade_day(current_date):
            return bond_day, None, None

        table_name = current_date.strftime('%Y%m%d')

        # 交易代码
        code = BondDB.query(table_name, "代码", conditions['ratio_total'])
        if code == -1:
            print(f"\n{current_date} 数据缺失")
            return bond_day, None, None
        elif code:
            total = len(code)
            data_remain = BondDB.query(table_name, "代码", conditions)
            remain = len(data_remain)
            return bond_day, remain, total

    @classmethod
    def bond_math(cls, current_date, column, conditions, model='median'):
        """
        计算中位数、平均数

        :param current_date: 日期
        :param column: 需要计算的列
        :param conditions: sql
        :param model: median,avg
        :return: 元组(日期, 中位数/平均数)
        """
        bond_day = current_date.strftime('%Y-%m-%d')
        if not api.is_trade_day(current_date):
            return bond_day, None

        table_name = current_date.strftime('%Y%m%d')

        # 交易代码
        data = BondDB.query(table_name, column, conditions)
        if data == -1:
            print(f"\n{current_date} 数据缺失")
            return bond_day, None
        # 判断数据是否为空
        elif len(data) == 0:
            return bond_day, '-'

        try:
            if model == 'median':
                return bond_day, np.median(data)
            elif model == 'avg':
                return bond_day, np.mean(data)
            elif model == 'max':
                return bond_day, max(data)
            elif model == 'min':
                return bond_day, min(data)
            elif model == 'std_0':
                # 有偏样本标准差
                return bond_day, np.std(data, ddof=0)
            elif model == 'std_1':
                # 无偏样本标准差
                return bond_day, np.std(data, ddof=1)
        except Exception as e:
            print('\n', '出现异常', e)
            print(data)
