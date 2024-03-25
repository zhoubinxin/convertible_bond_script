import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BondDB(object):
    def __init__(self, db_path='sqlite:///convertible_bond.db'):
        self.db_path = db_path

    def create_table(self):
        # 建立SQLite数据库连接
        engine = create_engine(self.db_path)

        # 创建inspect对象
        inspector = inspect(engine)

        # 遍历文件夹中的CSV文件
        folder_path = r'D:\Code\convertible_bond\Convertible_bonds\data'
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                table_name = file.split('.')[0]  # 使用文件名作为表名
                # 检查数据库中是否已经存在相应的表
                if not inspector.has_table(table_name):
                    # 如果数据库中不存在相应的表，则导入CSV文件内容
                    df = pd.read_csv(os.path.join(folder_path, file))
                    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        # 关闭数据库连接
        engine.dispose()

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
    # bonds = bond_db.get_all_bonds()
    # for bond in bonds:
    #     print(bond)
