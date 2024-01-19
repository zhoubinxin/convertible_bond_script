# 原json文件数据格式
#  [
#   "table":{
#       "jydm":[],
#       "p00868_f027":[],
#       "p00868_f022":[]
#   },
#  "ths_bond_balance_cbond":[],
#  "ths_issue_credit_rating_cbond":[]
#  ]
# 修改为如下格式 code为交易代码 cv为转股价值 cpr为转股溢价率 balance为债券余额 issue为债券评级
#  {
#   "code":[],
#   "cv":[],
#   "cpr":[],
#   "balance":[],
#   "issue":[]
#   }
import os
import json


def process_json_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)

            # 读取原始JSON文件
            with open(file_path, 'r') as file:
                original_data = json.load(file)

            # 处理原始数据
            processed_data = process_data(original_data)

            # 替换原JSON文件
            with open(file_path, 'w') as file:
                json.dump(processed_data, file, indent=2)


def process_data(original_data):
    result_data = {
        "code": [],
        "cv": [],
        "cpr": [],
        "balance": [],
        "issue": []
    }

    if isinstance(original_data, list):
        # 处理列表中的每个元素
        for item in original_data:
            # 根据元素的结构进行处理
            table_data = item.get("table", {})
            result_data["code"].extend(table_data.get("jydm", []))

            # 转换p00868_f027和p00868_f022的值为float类型
            cv_values = [float(value) if value != "--" else None for value in table_data.get("p00868_f027", [])]
            cpr_values = [float(value) if value != "--" else None for value in table_data.get("p00868_f022", [])]

            result_data["cv"].extend(cv_values)
            result_data["cpr"].extend(cpr_values)

            # 判断字段是否存在
            if "ths_bond_balance_cbond" in item:
                result_data["balance"].extend(item["ths_bond_balance_cbond"])

            if "ths_issue_credit_rating_cbond" in item:
                result_data["issue"].extend(item["ths_issue_credit_rating_cbond"])

    # 如果balance和issue字段都为空列表，则移除它们
    if not result_data["balance"]:
        del result_data["balance"]

    if not result_data["issue"]:
        del result_data["issue"]

    return result_data


# 替换为你的"data"目录路径
directory_path = "D:/Code/Pycharm/CPR/Test/data"

process_json_files(directory_path)
print("数据文件修改成功")
