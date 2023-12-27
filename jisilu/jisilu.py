import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_to_excel(data):
    # 将数据转换为DataFrame
    columns = [
        "行号", "操作", "代码", "转债名称", "现价", "涨跌幅", "正股代码", "正股名称", "正股价", "正股涨跌", "正股PB",
        "转股价",
        "转股价值", "转股溢价率", "双低", "纯债价值", "评级", "期权价值", "正股波动率", "回售触发价", "强赎触发价",
        "转债流通市值占比", "基金持仓", "到期时间", "剩余年限", "剩余规模(亿元)", "成交额(万元)", "换手率",
        "到期税前收益", "回售收益"
    ]
    data = data[1:]

    df = pd.DataFrame(data, columns=columns)

    # 保存数据到Excel文件
    excel_file_path = 'Data_jisilu.xlsx'
    df.to_excel(excel_file_path, index=False)


def extract_data(username, password):
    login_url = 'https://www.jisilu.cn/account/login/'
    browser = webdriver.Chrome()
    browser.get(login_url)

    wait = WebDriverWait(browser, 20)

    input_username = wait.until(EC.visibility_of_element_located((By.NAME, 'user_name')))
    input_username.send_keys(username)

    input_password = wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
    input_password.send_keys(password)

    agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.user_agree input')))
    agree_button.click()

    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-jisilu')))
    login_button.click()

    time.sleep(5)

    cb_list_url = 'https://www.jisilu.cn/web/data/cb/list'
    browser.get(cb_list_url)

    time.sleep(5)

    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr')))
    data = []
    for element in elements:
        data.append(element.text.split())

    browser.quit()

    return data


def main():
    username = ''
    password = ''

    data = extract_data(username, password)
    save_to_excel(data)


if __name__ == '__main__':
    main()
