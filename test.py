import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
from fake_useragent import UserAgent

ALPHA_LOGIN_URL = 'https://private.auth.alfabank.ru/passport/cerberus-mini-blue/dashboard-blue/phone_auth?response_type=code&client_id=newclick-web&scope=openid%20newclick-web&non_authorized_user=true'

proxy_list = [
    '78.37.254.43',
    '178.178.218.94',
    '178.204.20.202',
]


def get_random_user_agent():
    ua = UserAgent()
    return ua.random


def get_random_proxy():
    return random.choice(proxy_list)


def authenticate(account) -> None:
    """Авторизация в личном кабинете банка."""

    options = ChromeOptions()
    user_agent = get_random_user_agent()
    # proxy = get_random_proxy()
    # options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # Раскомментировать, если не нужно видеть работу браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9222")

    driver = Chrome(options=options)
    driver.get(ALPHA_LOGIN_URL)

    try:
        # if account.get_cookies():
        #     for cookie in account.get_cookies():
        #         driver.add_cookie(cookie)
        #     driver.refresh()
        # else:

        # Вводим номер телефона
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='phoneInput']"))
        )
        phone_input.send_keys(f"{account['phone_number'][1:]}")
        phone_input.send_keys(Keys.TAB)  # Пропустить к следующему элементу

        # Кликаем на кнопку "Вперёд"
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.phone-auth-browser__submit-button"))
        )
        time.sleep(0.05)
        submit_button.submit()

        # Вводим номер карты
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='card-account-input']"))
        )
        card_input.send_keys(account['card_number'])

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='card-account-continue-button']"))
        )
        time.sleep(0.05)
        continue_button.click()

        # Ожидаем, пока пользователь введет временный код через Django Admin
        while not account['temporary_code']:
            pass

        # Вводим одноразовый код
        otp_inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.code-input__input_1yhze"))
        )

        for index, digit in enumerate(account['temporary_code']):
            otp_inputs[index].send_keys(digit)

        # Ждем завершения авторизации
        # WebDriverWait(driver, 15).until(
        #     EC.url_contains("dashboard")
        # )

        # Сохраняем cookies
        account['session'] = driver.get_cookies()

        if not account['is_authenticated']:
            account['is_authenticated'] = True

        print(account)

        # while True:
        #     pass
        time.sleep(5)

    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
    finally:
        driver.close()
        driver.quit()

    return None


account = {
    'phone_number': '79102322910',
    'card_number': '2200150586033075',
    'temporary_code': '1234',
    'is_authenticated': False,
}

# authenticate(account)

for i in range(10):
    authenticate(account)
