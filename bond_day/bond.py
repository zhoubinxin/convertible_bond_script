from sqlalchemy import create_engine, and_, Column, String, Float
from sqlalchemy.orm import sessionmaker


class Bond(object):
    __tablename__ = None

    code = Column(String, primary_key=True)  # 代码
    name = Column(String)  # 名称
    trade_date = Column(String)  # 交易日期
    pcp = Column(Float)  # 前收盘价 previous closing price

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Bond({self.code})"

    @classmethod
    def query_data(cls, table_name):
        Bond.__tablename__ = table_name

        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'convertible_bond'
        }

        # 建立数据库连接
        engine = create_engine('mysql+pymysql://{user}:{password}@{host}/{database}'.format(**db_config))

        # 创建会话工厂
        Session = sessionmaker(bind=engine)

        # 创建会话
        session = Session()

        bonds = session.query(Bond).filter(and_(Bond.pcp > 1, Bond.pcp < 5)).all()
        if bonds:
            for bond in bonds:
                print(bond)
        else:
            print("Bond not found")

        # 关闭会话
        session.close()


def main():
    Bond.query_data('20180101')


if __name__ == '__main__':
    main()
