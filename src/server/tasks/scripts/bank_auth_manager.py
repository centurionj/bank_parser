import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions
from fake_useragent import UserAgent

from server.settings.config import ALPHA_LOGIN_URL

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def authenticate(account) -> None:
    """Авторизация в личном кабинете банка."""

    options = ChromeOptions()
    user_agent = get_random_user_agent()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # Раскомментировать, если не нужно видеть работу браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=43047")

    # driver = Chrome(
    #     options=options,
    #     driver_executable_path='/usr/bin/chromedriver'
    # )
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)

    driver.get(ALPHA_LOGIN_URL)

    try:
        if account.get_cookies():
            for cookie in account.get_cookies():
                driver.add_cookie(cookie)
            driver.refresh()

        # Вводим номер телефона

        phone_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='phoneInput']"))
        )
        phone_input.send_keys(str(account.phone_number)[1:])
        phone_input.send_keys(Keys.TAB)

        # Кликаем на кнопку "Вперёд"
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.phone-auth-browser__submit-button"))
        )
        time.sleep(1)
        submit_button.submit()

        # Вводим номер карты

        time.sleep(1)
        card_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='card-account-input']"))
        )
        card_input.send_keys(account.card_number)

        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='card-account-continue-button']"))
        )
        time.sleep(1)
        continue_button.click()


        # Ожидаем, пока пользователь введет временный код через Django Admin
        while not account.temporary_code:
            pass

        # Вводим одноразовый код
        time.sleep(1)
        otp_inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.code-input__input_1yhze"))
        )

        for index, digit in enumerate(account.temporary_code):
            otp_inputs[index].send_keys(digit)

        # Ждем завершения авторизации
        # WebDriverWait(driver, 15).until(
        #     EC.url_contains("dashboard")
        # )

        # Сохраняем cookies если не было сессии (здесь идет лок на апгрей кода в будущем)
        # if not account.session_cookies:
        #     account.set_cookies(driver.get_cookies())

        if not account.is_authenticated:
            account.is_authenticated = True
            account.save(update_fields=["is_authenticated"])

        time.sleep(20)

    except Exception as e:
        print(f"Ошибка при авторизации: {str(e)}")
        account.is_errored = True
        account.save(update_fields=["is_errored"])
    finally:
        driver.close()
        driver.quit()
