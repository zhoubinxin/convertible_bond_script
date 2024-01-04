from datetime import datetime
from nicegui import ui
from fastapi import FastAPI
from starlette.responses import RedirectResponse
import iFind
import jisilu
import Wind
from WindPy import w

app = FastAPI()
user = None


@ui.page('/')
def index():
    ui.button('同花顺数据接口', on_click=lambda: ui.open('/ifind'))
    ui.button('Wind数据接口', on_click=lambda: ui.open('/wind'))
    ui.button('集思录数据', on_click=lambda: ui.open('/jisilu'))


@ui.page('/ifind')
def ifind_page():
    def ifind():
        ui.notify('程序开始运行', type='positive')

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
        interval_data = iFind.get_interval_data(start, end)

        for date, data in interval_data:
            median_value = iFind.calculate_median(data.data[0]['table'], date, userdata)
            if median_value is not None:
                iFind.save_to_excel("转股溢价率记录.xlsx", date, median_value)

        ui.notify('程序结束运行', type='positive')

    ui.link('首页', '/')
    # 项目信息
    ui.link('CPR on GitHub', 'https://github.com/zhoubinxin/CPR')
    # 判断是否登录
    if user is None:
        return RedirectResponse(url="/login_ifind")

    with ui.splitter(value=100) as splitter:
        with splitter.before:
            ui.label('时间（YYYYMMDD）')
            with ui.row():
                start_date = ui.input('开始时间')
                end_date = ui.input('结束时间')
                ui.separator()

            ui.label('转换价值')
            with ui.row():
                consider_value = ui.checkbox('是否筛选')
                max_value = ui.input('最大值')
                min_value = ui.input('最小值')
                ui.separator()

            ui.label('债券余额范围')
            with ui.row():
                consider_balance = ui.checkbox('是否筛选')
                max_balance = ui.input('最大值')
                min_balance = ui.input('最小值')
                ui.separator()

            ui.label('债券评级')
            with ui.row():
                consider_issue = ui.checkbox('是否筛选')
                issue = ui.input('债券评级')
                ui.separator()

            ui.button('开始', on_click=ifind)

    with ui.header(elevated=True).style('background-color: #76aadb').classes('items-center justify-between'):
        ui.label('CPR').add_resource('/')

    with ui.footer().style('background-color: #76aadb'):
        ui.label('Power by NiceGUI')


@ui.page('/login_ifind')
def login_page():
    def try_login():
        global user
        is_login = iFind.login(username.value, password.value)
        if is_login == 0:
            user = username.value
            ui.notify(f'用户 {user} 登录成功')
            ui.open('/ifind')
        else:
            ui.notify(f'登录失败：{is_login}')

    with ui.card().classes('absolute-center'):
        username = ui.input('用户名').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('登录', on_click=try_login)


@ui.page('/wind')
def wind_page():
    def wind():
        ui.notify('程序开始运行', type='positive')

        w.start()

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
        interval_data = Wind.get_interval_data(start, end)

        for date, name, data in interval_data:
            median_value = Wind.calculate_median(data, name, date,userdata)
            if median_value is not None:
                Wind.save_to_excel("转股溢价率记录(Wind).xlsx", date, median_value)

        ui.notify('程序结束运行', type='positive')

    ui.link('首页', '/')
    # 项目信息
    ui.link('CPR on GitHub', 'https://github.com/zhoubinxin/CPR')

    with ui.splitter(value=80) as splitter:
        with splitter.before:
            ui.label('时间（YYYYMMDD）')
            with ui.row():
                start_date = ui.input('开始时间')
                end_date = ui.input('结束时间')
                ui.separator()

            ui.label('转换价值')
            with ui.row():
                consider_value = ui.checkbox('是否筛选')
                max_value = ui.input('最大值')
                min_value = ui.input('最小值')
                ui.separator()

            ui.label('债券余额范围')
            with ui.row():
                consider_balance = ui.checkbox('是否筛选')
                max_balance = ui.input('最大值')
                min_balance = ui.input('最小值')
                ui.separator()

            ui.label('债券评级')
            with ui.row():
                consider_issue = ui.checkbox('是否筛选')
                issue = ui.input('债券评级')
                ui.separator()

            ui.button('开始', on_click=wind)
        with splitter.after:
            ui.label('目前只支持转股价值的筛选')

    with ui.header(elevated=True).style('background-color: #76aadb').classes('items-center justify-between'):
        ui.label('CPR').add_resource('/')

    with ui.footer().style('background-color: #76aadb'):
        ui.label('Power by NiceGUI')


@ui.page('/jisilu')
def jisilu_page():
    def jsl():
        data = jisilu.extract_data(username.value, password.value)
        jisilu.save_to_excel(data)

    ui.link('首页', '/')
    ui.link('CPR on GitHub', 'https://github.com/zhoubinxin/CPR')
    username = ui.input('用户名')
    password = ui.input('密码')
    ui.button('确定', on_click=jsl)

    ui.label('目前仅实现对集思录可转载数据的抓取，未计算中位数')


ui.run(title='CPR')
