import pandas as pd
import os

data_median2 = [
    ("日期", "转股溢价率%"),
    ("2012-01-01", 0.02),
    ("2012-01-02", 0.03),
    ("2012-01-03", 0.04),
    ("2012-01-04", 0.05)
]

df = pd.DataFrame(data_median2[1:], columns=data_median2[0])

# 检查文件是否存在
if os.path.isfile('data.xlsx'):
    existing_data = pd.read_excel('data.xlsx')
    df = pd.concat([existing_data, df], ignore_index=True)

# 将数据写入 Excel 文件
with pd.ExcelWriter('data.xlsx', mode='w', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
