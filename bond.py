import datetime

from tqdm import tqdm

from bond_day import BondDay


# from convertible_bond import convertible_bond as cb
# from convertible_bond import filehandler as fh
# from convertible_bond import mysqlhandler as mysql


def main():
    # 起始日期
    start_date = datetime.date(2023, 2, 1)
    # 结束日期
    end_date = datetime.date(2023, 2, 3)

    # 具体设置参考 配置.md
    ctype = "avg"
    # 使用 calculate_math 函数需要填入列名
    column = "涨跌幅(%)"

    # 文件名（可选）
    file_name = ""

    # 筛选条件
    conditions = {
        "main": [
            "债券类型 = '可转债'",
            "`纯债到期收益率(%)` > 3",
            "((`转换价值` - `纯债价值`) / `纯债价值`) > 0.2"
        ],
        # 按 sort 进行排序，默认为升序，填 None 则不排序
        "sort": "涨跌幅(%)",
        # desc 表示降序
        "sort_type": "",
        # limit 表示限制返回的行数，-1 表示不限制
        "limit": 10,
        # 以上参数对 calculate_ratio 函数返回的转债总数不产生影响

        "ratio_total": [
            "债券类型 = '可转债'"
        ]
    }

    name_list = {
        "ratio": ("日期", "纯债到期收益率 > 3% 的转债个数", "转债总数"),
        "median": ("日期", "中位数"),
        "avg": ("日期", "平均数"),
        "max": ("日期", "最大值"),
        "min": ("日期", "最小值"),
        "std_0": ("日期", "有偏样本标准差"),
        "std_1": ("日期", "无偏样本标准差"),
        "check": ("数据表", "缺失数据"),
    }

    # 文件名附加日期
    if start_date == end_date:
        excel_name = file_name + str(start_date)
    else:
        excel_name = file_name + str(start_date) + "~" + str(end_date)

    # 设置列名
    try:
        data_list = [name_list[ctype]]
    except KeyError:
        print("不存在方法：", ctype)
        return

    # 更新数据
    BondDay.update()

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
        for current_date in range(total_days):
            current_date = start_date + datetime.timedelta(days=current_date)

            str_date = current_date.strftime('%Y%m%d')
            pbar.set_postfix_str(str_date)

            # 计算数据
            if ctype == "ratio":
                data_tuple = cb.calculate_ratio(current_date, conditions)
            elif ctype == "check":
                data_tuple = mysql.is_complete(current_date)
            else:
                if column == "":
                    column = input("请输入列名：")
                data_tuple = cb.calculate_math(current_date, column, conditions, ctype)

            if data_tuple:
                data_list.append(data_tuple)
            pbar.update(1)

    # 保存数据到Excel
    if len(data_list) > 1:
        fh.save_tuple_to_excel(excel_name, data_list)


if __name__ == '__main__':
    main()
