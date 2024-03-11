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
