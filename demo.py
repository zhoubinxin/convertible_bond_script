import json
import os
from datetime import datetime

from bond_day import BondDay


def main():
    # 配置文件地址
    config_list = [

    ]

    # 配置文件目录
    src_dir = 'config'
    file_list = os.listdir(src_dir)
    json_files = [file for file in file_list if file.endswith('.json')]

    config_list.extend(json_files)
    for config_file in config_list:
        parse(config_file)


def parse(config_file):
    # 读取JSON配置文件
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    # 起始日期
    start_date_str = config['start_date']
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    # 结束日期
    end_date_str = config["end_date"]
    end_date = datetime.strptime(end_date_str, "%Y%m%d")

    ctype = config["ctype"]
    column = config["column"]

    # 文件名
    file_name = config["file_name"]

    # 筛选条件
    conditions = config["conditions"]
    if conditions["limit"] != -1:
        print(f'仅返回前{conditions["limit"]}条数据')

    update = config["update"]

    column_name = config["column_name"]

    # 文件名附加日期
    if start_date == end_date:
        excel_name = file_name + start_date_str
    else:
        excel_name = file_name + start_date_str + "~" + end_date_str

    # 设置列名
    try:
        data_list = [column_name[ctype]]
    except KeyError:
        print("不存在方法：", ctype)
        return

    BondDay.db_init()

    # total_days = (end_date - start_date).days + 1
    # with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
    #     for current_date in range(total_days):
    #         current_date = start_date + timedelta(days=current_date)
    #
    #         str_date = current_date.strftime('%Y%m%d')
    #         pbar.set_postfix_str(str_date)
    #
    #         # 计算数据
    #         if ctype == "ratio":
    #             data_tuple = cb.calculate_ratio(current_date, conditions)
    #         elif ctype == "check":
    #             data_tuple = mysql.is_complete(current_date)
    #         else:
    #             if column == "":
    #                 column = input("请输入列名：")
    #             data_tuple = cb.calculate_math(current_date, column, conditions, ctype)
    #
    #         if data_tuple:
    #             data_list.append(data_tuple)
    #         pbar.update(1)
    #
    # # 保存数据到Excel
    # if len(data_list) > 1:
    #     fh.save_tuple_to_excel(excel_name, data_list)


if __name__ == '__main__':
    main()
