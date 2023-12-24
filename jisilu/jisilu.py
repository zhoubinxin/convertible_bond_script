from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(username, password):
    login_url = 'https://www.jisilu.cn/account/login/'
    browser = webdriver.Chrome()
    browser.get(login_url)

    wait = WebDriverWait(browser, 10)

    input_username = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="user_name"]')))
    input_username.send_keys(username)

    input_password = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="password"]')))
    input_password.send_keys(password)

    agree_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="user_agree"]/input')))
    agree_button.click()

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-jisilu"]')))
    login_button.click()

    return browser


def extract_data(browser):
    data_url = 'https://www.jisilu.cn/web/data/cb/list'
    browser.get(data_url)

    wait = WebDriverWait(browser, 10)

    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@title,"开始转股")]')))

    for element in elements:
        print(element.text)

    browser.quit()


def main():
    username = ''
    password = ''

    browser = login(username, password)

    extract_data(browser)


if __name__ == '__main__':
    main()
