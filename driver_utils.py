from moduls import *


def driversetting(headless_checked):
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent.random}")
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  # navigatoer.webdriver = False로 변경하기

    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

    options.add_argument('--disable-logging')
    # origin 허용(동적데이터 불러오기)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.headless = headless_checked
    driver = uc.Chrome(options=options)

    return driver


# naver 로그인
def naver_login(driver, wait, naver_id, naver_pw):
    tag_id = wait.until(EC.presence_of_element_located((By.NAME, 'id')))
    tag_id.click()
    pyperclip.copy(naver_id)
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    tag_pw = wait.until(EC.presence_of_element_located((By.NAME, 'pw')))
    tag_pw.click()
    pyperclip.copy(naver_pw)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 아이피 보안
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ip_text'))).click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, 'scr_ip3'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@onclick='javascript:dosubmit();']"))).click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    # 로그인 버튼을 클릭
    login_btn = wait.until(EC.presence_of_element_located((By.ID, 'log.login')))
    login_btn.click()
    time.sleep(1)
    return wait, driver


def driver_close(driver):
    # 현재 열려 있는 모든 창의 핸들을 가져옵니다.
    window_handles = driver.window_handles
    # 각 창을 하나씩 닫습니다.
    for handle in window_handles:
        driver.switch_to.window(handle)
        driver.close()
    driver.quit()