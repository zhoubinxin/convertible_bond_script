"""
将csv数据文件导入mysql

可转债csv数据获取：https://github.com/ZhouBinxin/Convertible_bonds
"""
import os
import pandas as pd
from sqlalchemy import create_engine, inspect

# MySQL数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'convertible_bond'
}

# 建立数据库连接
engine = create_engine('mysql+pymysql://{user}:{password}@{host}/{database}'.format(**db_config))

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
