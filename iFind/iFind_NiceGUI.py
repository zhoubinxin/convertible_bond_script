from datetime import datetime

from nicegui import ui
from fastapi import FastAPI
from starlette.responses import RedirectResponse
import iFind_For_GUI as bx

app = FastAPI()
user = None


@ui.page('/')
def index():
    def ifind():
        ui.notify('程序开始运行')

        userdata = {
            'consider_value': consider_value.value,
            'max_value': max_value.value,
            'min_value': min_value.value,
            'consider_balance': consider_balance.value,
            'max_balance': max_balance.value,
            'min_balance': min_balance.value,
            'consider_issue': consider_issue.value,
            'issue': issue.value
        }

        start = datetime.strptime(start_date.value, "%Y%m%d").date()
        end = datetime.strptime(end_date.value, "%Y%m%d").date()
        interval_data = bx.get_interval_data(start, end)

        for date, data in interval_data:
            median_value = bx.calculate_median(data.data[0]['table'], date, userdata)
            if median_value is not None:
                bx.save_to_excel("转股溢价率记录.xlsx", date, median_value)

        ui.notify('程序结束运行')

    # 项目信息
    ui.label(f'Hello {user},Welcome to CPR!')
    ui.link('CPR on GitHub', 'https://github.com/zhoubinxin/CPR')
    # 判断是否登录
    if user is None:
        return RedirectResponse(url="/login")

    ui.label('时间（YYYYMMDD）')
    start_date = ui.input('开始时间')
    end_date = ui.input('结束时间')

    ui.label('转换价值')
    consider_value = ui.checkbox('是否筛选')
    max_value = ui.input('最大值')
    min_value = ui.input('最小值')

    ui.label('债券余额范围')
    consider_balance = ui.checkbox('是否筛选')
    max_balance = ui.input('最大值')
    min_balance = ui.input('最小值')

    ui.label('债券评级')
    consider_issue = ui.checkbox('是否筛选')
    issue = ui.input('债券评级')

    ui.button('开始', on_click=ifind)


@ui.page('/login')
def login_page():
    def try_login():
        global user
        is_login = bx.login(username.value, password.value)
        if is_login == 0:
            user = username.value
            ui.notify(f'用户 {user} 登录成功')
            ui.open('/')
        else:
            ui.notify(f'登录失败：{is_login}')

    with ui.card().classes('absolute-center'):
        username = ui.input('用户名').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('登录', on_click=try_login)


ui.run(title='CPR')
