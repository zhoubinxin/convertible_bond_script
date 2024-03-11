from . import bonddb


class Bond(object):
    def __init__(self):
        # self.name = name
        # self.cusip = cusip
        # self.face_value = face_value
        # self.coupon_rate = coupon_rate
        # self.maturity = maturity
        pass

    def __repr__(self):
        return f"Bond({self.name})"

    def query_data(self):
        database_url = 'mysql+pymysql://root:123456@localhost/convertible_bond'
        bond_db = bonddb.BondDB(database_url, '20180101')
        data = bond_db.query_data('`代码`')
        return data
