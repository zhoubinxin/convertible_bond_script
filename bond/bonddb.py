from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BondDB(object):
    def __init__(self, db_url, table_name):
        self.engine = create_engine(db_url, echo=True)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.table_name = table_name

    def query_data(self, column):
        Session = self.Session()
        try:
            # 获取表的元数据
            table_class = Base.metadata.tables[self.table_name]

            # 查询指定列的数据
            result = Session.query(table_class.c[column]).all()
            return result
        except Exception as e:
            print(f"查询出错: {str(e)}")
        finally:
            Session.close()


# 使用示例
if __name__ == "__main__":
    DATABASE_URL = "mysql+pymysql://root:123456@localhost/convertible_bond"
    bond_db = BondDB(DATABASE_URL, table_name='20180101')

    # 查询所有可转债数据
    bonds = bond_db.get_all_bonds()
    for bond in bonds:
        print(bond)
