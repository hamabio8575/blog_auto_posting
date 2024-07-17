from moduls import *
import driver_utils

try:
    naver_id = 'jiralma86'
    naver_pw = '!gkffhd9514'

    headless_checked = False
    driver = driver_utils.driversetting(headless_checked)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.naver.com")
    driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
    time.sleep(1)
    wait, driver = driver_utils.naver_login(driver, wait, naver_id, naver_pw)  # 로그인 함수


    driver.execute_script(f"window.open('https://blog.naver.com/jiralma86?Redirect=Write&', '_blank');")
    # 블로그 클릭
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'service_icon.type_blog'))).click()
    time.sleep(1)
    # 글쓰기 클릭
    driver.switch_to.window(driver.window_handles[-1])
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.default_content()  # 기본 iframe으로 복귀
    driver.switch_to.frame('mainFrame')
    time.sleep(1)
    soup = driver.page_source
    if "작성 중인 글이 있습니다." in soup:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-popup-button-text"))).click()
        time.sleep(3)


    # 복붙용 크롬창 열기 (실제로는 여기에 작성)
    driver.switch_to.window(driver.window_handles[-2])
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
    time.sleep(3)


    # 글쓰기 시작
    driver.switch_to.window(driver.window_handles[-2])
    time.sleep(1)
    driver.switch_to.default_content()  # 기본 iframe으로 복귀
    driver.switch_to.frame('mainFrame')

    time.sleep(3)
    if "작성 중인 글이 있습니다." in driver.page_source:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-popup-button-text"))).click()
        time.sleep(3)

    # 중요!!!! 브라우저 패널의 높이값
    panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')

    ### 제목 입력
    # 제목 입력 element
    # titel_input_box = driver.find_element(By.XPATH, """//span[text()='제목']""")
    titel_input_box = wait.until(EC.presence_of_element_located((By.XPATH, """//span[text()='제목']""")))
    # 제목 입력 element의 x 값 가져오기 (절대값)
    abs_x = titel_input_box.location['x']
    # 제목 입력 element의 y 값 가져오기 (상대값, 브라우저에 있는 y값)
    y = titel_input_box.location['y']
    abs_y = y + panel_height
    # 마우스 이동해서 클릭
    pyautogui.click(abs_x + 20, abs_y + 20)
    input()
except Exception as e:
    print(e)
    input()