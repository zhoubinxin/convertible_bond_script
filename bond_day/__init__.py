from . import api
from .bond import Bond


class BondDay(object):
    def __init__(self, trade_date):
        self.date = trade_date

    def __repr__(self):
        return '<Date: %s>' % self.date

    @classmethod
    def update(cls):
        """
        更新数据

        :return:
        """
        print('更新数据中...')
        api.update()
        print('更新完成')
        cls.update_executed = True

    @classmethod
    def calculate_ratio(cls, current_date, conditions):
        """
        计算比率

        :param current_date: 日期
        :param conditions: sql
        :return: 元组(日期, 筛选后剩余数量, 总数)
        """
        if not api.is_trade_day(current_date):
            return str(current_date), None, None

        str_date = current_date.strftime('%Y%m%d')

        # 交易代码
        code = mysql.get_data_from_mysql(str_date, "代码", conditions['ratio_total'])
        if code == -1:
            print(f"\n{current_date} 数据缺失")
            return str(current_date), None, None
        elif code:
            total = len(code)
            data_remain = mysql.get_data_from_mysql(str_date, "代码", conditions)
            remain = len(data_remain)
            return str(current_date), remain, total
