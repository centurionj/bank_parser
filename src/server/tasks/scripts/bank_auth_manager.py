import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions

from server.settings.config import ALPHA_LOGIN_URL


def authenticate(account):
    """Авторизация в личном кабинете банка."""

    options = ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Раскомментировать, если не нужно видеть работу браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = Chrome(
        options=options,
        driver_executable_path='/usr/bin/chromedriver'
    )
    driver.get(ALPHA_LOGIN_URL)

    try:
        if account.get_cookies():
            for cookie in account.get_cookies():
                driver.add_cookie(cookie)
            driver.refresh()

        # Вводим номер телефона
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='phoneInput']"))
        )
        phone_input.send_keys(str(account.phone_number)[1:])
        phone_input.send_keys(Keys.TAB)

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
        card_input.send_keys(account.card_number)

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='card-account-continue-button']"))
        )
        time.sleep(0.05)
        continue_button.click()

        # Ожидаем, пока пользователь введет временный код через Django Admin
        while not account.temporary_code:
            pass

        # Вводим одноразовый код
        otp_inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.code-input__input_1yhze"))
        )

        account.set_cookies(driver.get_cookies())

        for index, digit in enumerate(account.temporary_code):
            otp_inputs[index].send_keys(digit)

        # Ждем завершения авторизации
        WebDriverWait(driver, 15).until(
            EC.url_contains("dashboard")
        )

        # Сохраняем cookies если не было сессии (здесь идет лок на апгрей кода в будущем)
        if not account.session:
            account.session = driver.get_cookies()

        if not account.is_authenticated:
            account.is_authenticated = True
            account.save(update_fields=["is_authenticated"])

        time.sleep(20)

    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
    finally:
        driver.close()
        driver.quit()

    return driver
