# 纯债到期收益率大于x的转债个数/当天所有转债数
import datetime
from tqdm import tqdm
from convertible_bond import convertible_bond as cb
from convertible_bond import mysqlhandler as mysql
from convertible_bond import filehandler as fh


def main():
    # 数据周期
    start_date = datetime.date(2018, 1, 1)
    end_date = datetime.date(2018, 12, 31)

    data_consider = {
        # 转股价值
        "consider_cv": False,
        "cv_range": "",
        # 债券余额，单位为亿
        "consider_balance": False,
        "balance_range": "",
        # 债券评级
        "consider_issue": False,
        "issue": "",
        # 纯债到期收益率
        "consider_ytm": True,
        "ytm_range": "`纯债到期收益率(%)` > 3",
    }

    date_list = []
    data_sum = []
    data_ytm = []

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
        for current_date in range(total_days):
            current_date = start_date + datetime.timedelta(days=current_date)

            str_date = current_date.strftime('%Y%m%d')
            pbar.set_postfix_str(str_date)

            date_list.append(str_date)

            if current_date.weekday() in [5, 6]:
                data_ytm.append(None)
                data_sum.append(None)
                continue

            # 交易代码
            code = mysql.get_data_from_mysql(str_date, "代码")
            if code:
                data_sum.append(len(code))
                ytm = mysql.get_data_from_mysql(str_date, "代码", data_consider)
                data_ytm.append(len(ytm))
            elif code == -1:
                print(f"{str_date} 数据缺失")
                data_sum.append(None)
                data_ytm.append(None)

            pbar.update(1)

    data_dict = {
        "日期": date_list,
        f"纯债到期收益率 > 3% 的转债个数": data_ytm,
        "转债总数": data_sum
    }

    fh.save_to_excel("纯债到期收益率个数", data_dict)


if __name__ == '__main__':
    main()
