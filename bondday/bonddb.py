import datetime
import os

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BondDB(object):
    @classmethod
    def init(cls, database='convertible_bond'):
        # 建立SQLite数据库连接
        engine = create_engine(f'sqlite:///{database}.db')

        # 创建inspect对象
        inspector = inspect(engine)

        # 遍历文件夹中的CSV文件
        folder_path = '../Convertible_bonds/data'
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

    @classmethod
    def query(cls, table, column, conditions, database='convertible_bond'):
        # 建立SQLite数据库连接
        engine = create_engine(f'sqlite:///{database}.db')

        # 构建查询语句
        query = f"SELECT `{column}` FROM `{table}`"

        if 'main' in conditions:
            conditions['main'].append(f"`{column}` is not null")
            query += " WHERE " + " AND ".join(conditions['main'])

            # 排序
            if 'sort' in conditions and conditions['sort'] is not None:
                query += f" ORDER BY `{conditions['sort']}`"
            if 'sort_type' in conditions and conditions['sort_type'] == 'desc':
                query += " desc"

            # 限制返回数量
            if 'limit' in conditions and conditions['limit'] != -1:
                if conditions['limit'] <= 0:
                    print(" limit 必须大于 0")
                else:
                    query += f" LIMIT {conditions['limit']}"
        else:
            conditions.append(f"`{column}` is not null")
            query += " WHERE " + " AND ".join(conditions)

        try:
            df = pd.read_sql_query(query, con=engine)
            data_bond = df.values.tolist()
        except sqlalchemy.exc.OperationalError as e:
            error_message = str(e)

            if "no such table" in error_message:
                # 数据表不存在
                data_bond = -1
            elif "no such column" in error_message:
                # 列不存在
                data_bond = -2
            else:
                data_bond = -3

        # 关闭数据库连接
        engine.dispose()

        return data_bond


# 使用示例
if __name__ == "__main__":
    conditions = {
        "main": [
            "债券类型 = '可转债'",
            "`纯债到期收益率(%)` > 3",
            "((`转换价值` - `纯债价值`) / `纯债价值`) > 0.2"
        ],
        "sort": None,
        "sort_type": "",
        "limit": -1,
        "ratio_total": [
            "债券类型 = '可转债'"
        ]
    }
    bond_day = datetime.date.today()
    data = BondDB.query(bond_day, '码', conditions=conditions["main"],
                        database='D:\Code\convertible_bond\convertible_bond_script\convertible_bond')
    print(data)
