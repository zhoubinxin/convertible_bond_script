import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
import pandas as pd
from iFinDPy import *
import datetime
import time


def login(username, password):
    # 模拟登录函数
    thsLogin = THS_iFinDLogin(username, password)
    if thsLogin != 0:
        return False
    else:
        return True


def toggle_password_visibility():
    if show_password_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")


def check_credentials():
    username = entry_username.get()
    password = entry_password.get()

    if login(username, password):
        remember_credentials(username, password)
        root.destroy()
        show_dashboard(username)
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")


def remember_credentials(username, password):
    credentials = {'username': username, 'password': password}
    with open('credentials.pkl', 'wb') as file:
        pickle.dump(credentials, file)


def get_saved_credentials():
    if os.path.exists('credentials.pkl'):
        with open('credentials.pkl', 'rb') as file:
            credentials = pickle.load(file)
            return credentials.get('username', ''), credentials.get('password', '')
    return '', ''


def show_dashboard(username):
    dashboard = tk.Tk()
    dashboard.title("用户" + username)
    dashboard.geometry("400x500")  # 调整窗口大小

    def on_confirm():
        global max_value, min_value, max_balance, min_balance, issue, start_date, end_date
        global consider_value, consider_balance, consider_issue

        consider_value = value_check_var.get()
        consider_balance = balance_check_var.get()
        consider_issue = issue_check_var.get()
        consider_day = date_check_var.get()

        max_value = float(max_value_input.get()) if max_value_input.get() else float('inf')
        min_value = float(min_value_input.get()) if min_value_input.get() else 0.0
        max_balance = float(max_balance_input.get()) if max_balance_input.get() else float('inf')
        min_balance = float(min_balance_input.get()) if min_balance_input.get() else 0.0
        issue = issue_input.get()
        start_date = start_date_input.get()
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d").date()
        if consider_day:
            end_date = start_date
        else:
            end_date = end_date_input.get()
            end_date = datetime.datetime.strptime(end_date, "%Y%m%d").date()

        dashboard.destroy()  # 关闭窗口

    def enable_disable_entries():
        # 根据复选框状态启用或禁用输入框
        if value_check_var.get():
            max_value_input.config(state='normal')
            min_value_input.config(state='normal')
        else:
            max_value_input.delete(0, tk.END)
            min_value_input.delete(0, tk.END)
            max_value_input.config(state='disabled')
            min_value_input.config(state='disabled')

        if balance_check_var.get():
            max_balance_input.config(state='normal')
            min_balance_input.config(state='normal')
        else:
            max_balance_input.delete(0, tk.END)
            min_balance_input.delete(0, tk.END)
            max_balance_input.config(state='disabled')
            min_balance_input.config(state='disabled')

        if issue_check_var.get():
            issue_input.config(state='normal')
        else:
            issue_input.delete(0, tk.END)
            issue_input.config(state='disabled')

        if date_check_var.get():
            start_date_input.config(state='normal')
            end_date_input.config(state='disabled')
            end_date_input.delete(0, tk.END)
            end_date_input.insert(0, start_date_input.get())
        else:
            start_date_input.config(state='normal')
            end_date_input.config(state='normal')

    value_frame = tk.LabelFrame(dashboard, text="转股价值筛选")
    value_frame.pack(padx=10, pady=10, fill="both", expand="yes")

    value_check_var = tk.BooleanVar()
    value_check = tk.Checkbutton(value_frame, text="是否筛选转股价值", variable=value_check_var,
                                 command=enable_disable_entries)
    value_check.grid(row=0, column=0, columnspan=2)

    max_value_label = tk.Label(value_frame, text="最大价值")
    max_value_label.grid(row=1, column=0)
    max_value_input = tk.Entry(value_frame, state='disabled')  # 默认禁用输入框
    max_value_input.grid(row=1, column=1)

    min_value_label = tk.Label(value_frame, text="最小价值")
    min_value_label.grid(row=2, column=0)
    min_value_input = tk.Entry(value_frame, state='disabled')  # 默认禁用输入框
    min_value_input.grid(row=2, column=1)

    balance_frame = tk.LabelFrame(dashboard, text="债券余额筛选")
    balance_frame.pack(padx=10, pady=10, fill="both", expand="yes")

    balance_check_var = tk.BooleanVar()
    balance_check = tk.Checkbutton(balance_frame, text="是否筛选债券余额", variable=balance_check_var,
                                   command=enable_disable_entries)
    balance_check.grid(row=0, column=0, columnspan=2)

    max_balance_label = tk.Label(balance_frame, text="最大值")
    max_balance_label.grid(row=1, column=0)
    max_balance_input = tk.Entry(balance_frame, state='disabled')  # 默认禁用输入框
    max_balance_input.grid(row=1, column=1)

    min_balance_label = tk.Label(balance_frame, text="最小值")
    min_balance_label.grid(row=2, column=0)
    min_balance_input = tk.Entry(balance_frame, state='disabled')  # 默认禁用输入框
    min_balance_input.grid(row=2, column=1)

    issue_frame = tk.LabelFrame(dashboard, text="债券评级筛选")
    issue_frame.pack(padx=10, pady=10, fill="both", expand="yes")

    issue_check_var = tk.BooleanVar()
    issue_check = tk.Checkbutton(issue_frame, text="是否筛选债券评级", variable=issue_check_var,
                                 command=enable_disable_entries)
    issue_check.grid(row=0, column=0, columnspan=2)

    issue_label = tk.Label(issue_frame, text="债券评级")
    issue_label.grid(row=1, column=0)
    issue_input = tk.Entry(issue_frame, state='disabled')  # 默认禁用输入框
    issue_input.grid(row=1, column=1)

    date_frame = tk.LabelFrame(dashboard, text="日期筛选")
    date_frame.pack(padx=10, pady=10, fill="both", expand="yes")

    date_check_var = tk.BooleanVar()
    date_check = tk.Checkbutton(date_frame, text="是否单日", variable=date_check_var, command=enable_disable_entries)
    date_check.grid(row=0, column=0, columnspan=2)

    start_date_label = tk.Label(date_frame, text="开始日期 (yyyymmdd)")
    start_date_label.grid(row=1, column=0)
    start_date_input = tk.Entry(date_frame)  # 开始日期始终可输入
    start_date_input.grid(row=1, column=1)

    end_date_label = tk.Label(date_frame, text="结束日期 (yyyymmdd)")
    end_date_label.grid(row=2, column=0)
    end_date_input = tk.Entry(date_frame)
    end_date_input.grid(row=2, column=1)

    confirm_button = tk.Button(dashboard, text="确定", command=on_confirm)
    confirm_button.pack()

    dashboard.mainloop()


def create_login_window():
    global entry_username, entry_password, show_password_var, root

    root = tk.Tk()
    root.title("登录")
    root.geometry("300x230")  # 调整窗口大小

    canvas = tk.Canvas(root, bg="#ffffff", width=300, height=230)
    canvas.pack()

    frame = tk.Frame(root, bg="#ffffff")
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    label_username = tk.Label(frame, text="用户名", bg="#ffffff", font=("Arial", 12))
    label_username.pack()
    entry_username = tk.Entry(frame, font=("Arial", 10))
    entry_username.pack()

    label_password = tk.Label(frame, text="密码", bg="#ffffff", font=("Arial", 12))
    label_password.pack()
    entry_password = tk.Entry(frame, show="*", font=("Arial", 10))
    entry_password.pack()

    show_password_var = tk.BooleanVar()
    show_password_checkbox = tk.Checkbutton(frame, text="显示密码", variable=show_password_var,
                                            command=toggle_password_visibility, bg="#ffffff", font=("Arial", 10))
    show_password_checkbox.pack()

    saved_username, saved_password = get_saved_credentials()
    entry_username.insert(0, saved_username)
    entry_password.insert(0, saved_password)

    login_button = tk.Button(frame, text="登录", command=check_credentials, bg="#4CAF50", fg="white",
                             font=("Arial", 12))
    login_button.pack()

    root.mainloop()


def get_data(edate):
    get_str = 'edate=' + edate + ';zqlx=全部'
    # jydm交易代码 f027转换价值 f022转股溢价率
    data_p00868 = THS_DR('p00868', get_str, 'jydm:Y,p00868_f027:Y,p00868_f022:Y', 'format:list')
    # print(data_p00868)
    if data_p00868.data is None:
        print(data_p00868.errmsg)

    return data_p00868


# 获取债券余额数据和债券评级
def get_bond(jydm, date):
    print("------------------债券余额数据和债券评级------------------")
    print(date)
    # ths_bond_balance_cbond债券余额数据 ths_issue_credit_rating_cbond债券评级
    data = THS_DS(jydm, 'ths_bond_balance_cbond;ths_issue_credit_rating_cbond', ';', '', date, date, 'format:list')

    if data.data is None:
        print(data.errmsg)
        return None, None

    return data.data[0]['table']['ths_bond_balance_cbond'][0], data.data[0]['table']['ths_issue_credit_rating_cbond']


# 保存数据到Excel
def save_to_excel(file_name, str_date, premium):
    print(f'数据保存中{str_date}')
    while True:
        try:
            if not os.path.exists(file_name):
                data = {"日期": [str_date], "转股溢价率%": [premium]}
                df = pd.DataFrame(data)
            else:
                df = pd.read_excel(file_name)
                new_data = pd.DataFrame({"日期": [str_date], "转股溢价率%": [premium]})
                df = pd.concat([df, new_data], ignore_index=True)

            df.to_excel(file_name, index=False)
            break  # 如果成功写入，跳出循环
        except PermissionError:
            print(f"请关闭文件 '{file_name}'")
            time.sleep(5)


# 计算中位数
def calculate_median(data, date):
    float_values = []

    data_jydm = data['jydm']
    data_f022 = data['p00868_f022']
    data_f027 = data['p00868_f027']

    for jydm, f027, f022 in zip(data_jydm, data_f027, data_f022):
        if '--' in f027 or '--' in f022:
            continue

        data_balance = None
        data_issue = None
        if consider_balance or consider_issue:
            data_balance, data_issue = get_bond(jydm, date)

        f027_value = float(f027)
        f022_value = float(f022)

        value_condition = (not consider_value) or (min_value < f027_value <= max_value)
        balance_condition = (not consider_balance) or (min_balance < data_balance)
        issue_condition = (not consider_issue) or (data_issue == issue)

        if value_condition and balance_condition and issue_condition:
            float_values.append(f022_value)

    return np.median(float_values) if float_values else ""


# 获取数据
def get_interval_data(start, end):
    delta = datetime.timedelta(days=1)
    data_list = []

    while start <= end:
        print(start)
        edate = start.strftime("%Y%m%d")
        data = get_data(edate)
        if data.data is not None:
            data_list.append((start.strftime("%Y-%m-%d"), data))
        start += delta

    return data_list


def main():
    create_login_window()

    interval_data = get_interval_data(start_date, end_date)

    for date, data in interval_data:
        median_value = calculate_median(data.data[0]['table'], date)
        # print(median_value)
        if median_value is not None:
            save_to_excel("转股溢价率记录.xlsx", date, median_value)


if __name__ == "__main__":
    main()
