from sqlalchemy import create_engine, Column, String, Float, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


class BondDB(object):
    def __init__(self, db_url, table_name):
        self.engine = create_engine(db_url, echo=True)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.table_name = table_name

    def create_table(self):
        self.Base.metadata.create_all(self.engine)

    def define_bond_class(self):
        class ConvertibleBond(self.Base):
            __tablename__ = self.table_name

            # 列名中的特殊字符使用反引号括起来
            code = Column(String, name='代码', primary_key=True)
            name = Column(String, name='名称')
            trade_date = Column(String, name='交易日期')
            previous_close_price = Column(Float, name='前收盘价')
            open_price = Column(Float, name='开盘价')
            highest_price = Column(Float, name='最高价')
            lowest_price = Column(Float, name='最低价')
            close_price = Column(Float, name='收盘价')
            rise_fall = Column(Float, name='涨跌')
            rise_fall_range = Column(Float, name='涨跌幅(%)')
            accrued_interest_days = Column(BigInteger, name='已计息天数')
            accrued_interest = Column(Float, name='应计利息')
            remain_term = Column(Float, name='剩余期限(年)')
            current_yield = Column(Float, name='当期收益率(%)')
            ytm = Column(Float, name='纯债到期收益率(%)')
            pure_bond_value = Column(Float, name='纯债价值')
            pure_bond_premium = Column(Float, name='纯债溢价')
            pure_bond_premium_ratio = Column(Float, name='纯债溢价率(%)')
            conversion_price = Column(Float, name='转股价格')
            conversion_ratio = Column(Float, name='转股比例')
            conversion_value = Column(Float, name='转换价值')
            conversion_premium = Column(Float, name='转股溢价')
            conversion_premium_rate = Column(Float, name='转股溢价率(%)')
            conversion_p2e_ratio = Column(Float, name='转股市盈率')
            conversion_p2b_ratio = Column(Float, name='转股市净率')
            arbitrage_space = Column(Float, name='套利空间')
            parity = Column(Float, name='平价/底价')
            term = Column(BigInteger, name='期限(年)')
            issue_date = Column(String, name='发行日期')
            coupon_rate = Column(Float, name='票面利率/发行参考利率(%)')
            trade_floor = Column(String, name='交易市场')
            bond_type = Column(String, name="债券类型")

        return ConvertibleBond

    def add_bond(self, bond_data):
        Session = self.Session()
        BondClass = self.define_bond_class()
        bond = BondClass(**bond_data)
        Session.add(bond)
        Session.commit()
        Session.close()

    def get_all_bonds(self):
        Session = self.Session()
        BondClass = self.define_bond_class()
        bonds = Session.query(BondClass).all()
        Session.close()
        return bonds


# 使用示例
if __name__ == "__main__":
    DATABASE_URL = "mysql+pymysql://root:123456@localhost/convertible_bond"
    bond_db = BondDB(DATABASE_URL, table_name='20180101')

    # 查询所有可转债数据
    bonds = bond_db.get_all_bonds()
    for bond in bonds:
        print(bond)
