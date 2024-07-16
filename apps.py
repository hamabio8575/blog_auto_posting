from moduls import *

import driver_utils
import posting_utils
import vpn_utils
import utils


### 주소 저장된 파일 선택 함수
def file_open(model):
    global path
    current_directory = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 파일의 경로
    path = QFileDialog.getExistingDirectory(model, '폴더 선택', current_directory)
    model.textBrowser.append(f"선택 폴더 -- {path}\n")


def go_run(model):
    logger, file_handler = utils.setup_logging()

    # 한/영키 확인
    utils.ko_eng_checked()

    today = datetime.today()
    today_date = utils.get_today_date()  # 오늘 날짜 확인 // format : 5월24일
    df = pd.read_excel("블로그 포스팅 세팅 파일.xlsx")
    df = df.iloc[:, :7]

    for number, naver_id, naver_pw, vpn_name, vpn_id, vpn_pw, p_title in df.to_numpy().tolist():
        try:

            start_time = time.time()
            if path:
                # 이미지 경로 생성
                image_folder_path = os.path.join(
                    path,
                    "자동업로드",
                    today_date,
                    '이미지',
                    p_title,
                )

                video_folder_path = os.path.join(
                    path,
                    "자동업로드",
                    today_date,
                    '영상',
                    p_title,
                )

                image_folder_path = os.path.normpath(image_folder_path)  # 이미지 경로 표준화
                video_folder_path = os.path.normpath(video_folder_path)  # 동영상 경로 표준화

            image_file_list = os.listdir(image_folder_path)
            img_file_len = len(image_file_list)

            video_file_list = os.listdir(video_folder_path)
            video_file_len = len(video_file_list)
            print(f"이미지 경로 : {image_folder_path}")
            print(f"이미지 파일들 : {image_file_list}")
            print(f"이미지 파일개수 : {img_file_len}")

            print()
            print(f"동영상 경로 : {video_folder_path}")
            print(f"이미지 파일들 : {video_file_list}")
            print(f"이미지 파일개수 : {video_file_len}")

            post_file_path = rf'{path}\자동업로드\{today_date}\원고\{p_title}.txt'
            post_file_path = os.path.normpath(post_file_path)  # 동영상 경로 표준화

            print()
            print(f"포스팅 원고파일 제목 : {post_file_path}")
            # 파일 읽기
            with open(post_file_path, 'r', encoding='utf-8') as file:
                file.seek(0)  # 파일 포인터를 파일의 처음으로 이동 (첫줄이 빈문자열로 나오는걸 방지하기 위함)
                post_title = file.readline().strip()
                original_post = file.read()
            # 출력 확인
            print(post_title)

            # mvpn 접속
            dlg = vpn_utils.mvpn_connect(model, vpn_id, vpn_pw)

            ### 네이버 로그인
            headless_checked = False
            try:
                driver = driver_utils.driversetting(headless_checked)
            except:
                print("☆ Error driver setting...")
                print("30초후 재개 됩니다.")
                time.sleep(30)
                driver = driver_utils.driversetting(headless_checked)

            driver.maximize_window()
            wait = WebDriverWait(driver, 10)
            driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
            time.sleep(1)
            wait, driver = driver_utils.naver_login(driver, wait, naver_id, naver_pw)  # 로그인 함수

            # 블로그 클릭
            # driver.find_element(By.CLASS_NAME, "service_icon.type_blog").click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'service_icon.type_blog'))).click()
            time.sleep(1)
            # 글쓰기 클릭
            driver.switch_to.window(driver.window_handles[-1])
            # driver.find_element(By.XPATH, "//a[text()='글쓰기']").click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
            time.sleep(10)
            # 글쓰기 시작
            driver.switch_to.window(driver.window_handles[-1])
            driver.switch_to.default_content()  # 기본 iframe으로 복귀
            driver.switch_to.frame('mainFrame')
            time.sleep(1)

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
            time.sleep(1)
            posting_utils.posting_run(post_title, image_folder_path, img_file_len, video_folder_path, video_file_len, driver, wait,
                        post_title, p_title)
            time.sleep(3)

            ### 본문 입력
            # 본문 입력 element
            pyautogui.press('hangul')
            contents_input_box = driver.find_element(By.CLASS_NAME,
                                                     "se-placeholder.__se_placeholder.se-ff-nanumgothic.se-fs15")
            # 본문 입력 element
            panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
            # 본문 입력 element의 x 값 가져오기 (절대값)
            abs_x = contents_input_box.location['x']
            # 본문 입력 element의 y 값 가져오기 (상대값, 브라우저에 있는 y값)
            y = contents_input_box.location['y']
            abs_y = y + panel_height
            pyautogui.click(abs_x + 20, abs_y + 20)
            time.sleep(3)
            pyautogui.press("T")
            # posting_run(original_post, image_folder_path, img_file_len, video_folder_path, video_file_len, driver, wait, post_title, p_title)

            # 도움말 있는지 체크
            # 도움말이 있으면 발행버튼이 안눌림
            if 'se-help-panel-close-button' in str(driver.page_source):
                print('있다')
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-help-panel-close-button"))).click()

            # 발행
            driver.find_element(By.XPATH, "//span[text()='발행']").click()
            time.sleep(3)
            driver.find_elements(By.XPATH, "//span[text()='발행']")[-1].click()

            time.sleep(3)
            for _ in range(len(driver.window_handles)):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                time.sleep(0.5)
            time.sleep(3)
            vpn_utils.mvpn_close(dlg)
            time.sleep(3)

            minutes, seconds = utils.get_lab_time(start_time)
            print(f"■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")
            model.textBrowser.append(f"■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")
            logger.debug(f"■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")

        except Exception as e:
            print(e)
            logger.error(f"■ [{number}] {post_title} 포스팅 실패")
            for _ in range(len(driver.window_handles)):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                time.sleep(0.5)
            try:
                vpn_utils.mvpn_close(dlg)
            except:
                pass