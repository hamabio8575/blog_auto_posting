from moduls import *

import driver_utils
import posting_utils
import vpn_utils
import utils
import downloaders
import file_open

# 파일들 사이즈 체크

# mvpn_id, mvpn_pw = "hama75", "hama123!"
# dlg = vpn_utils.mvpn_connect(downloaders.new_model, mvpn_id, mvpn_pw)
# time.sleep(3)
#
# vpn_utils.mvpn_close(dlg)


path = file_open.new_paht
print(path)
utils.file_size_check(path, downloaders.new_model)
logger, file_handler = utils.setup_logging()

# 한/영키 확인
utils.ko_eng_checked()

today = datetime.today()
today_date = utils.get_today_date()  # 오늘 날짜 확인 // format : 5월24일
df = pd.read_excel("블로그 포스팅 세팅 파일.xlsx")
df = df.iloc[:, :7]

while True:
    for number, naver_id, naver_pw, vpn_name, vpn_id, vpn_pw, p_title in df.to_numpy().tolist():
        # try:
        success_data_list = utils.get_log_data_for_success()
        print(success_data_list)
        print(p_title)
        if p_title in success_data_list:
            continue

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

            imageLink_folder_path = os.path.join(
                path,
                "자동업로드",
                today_date,
                '이미지링크',
                p_title,
            )

            multi_img_folder_path = os.path.join(
                path,
                "자동업로드",
                today_date,
                '멀티이미지',
                p_title,
            )

            image_folder_path = os.path.normpath(image_folder_path)  # 이미지 경로 표준화
            video_folder_path = os.path.normpath(video_folder_path)  # 동영상 경로 표준화
            imageLink_folder_path = os.path.normpath(imageLink_folder_path)  # 이미지링크 경로 표준화
            multi_img_folder_path = os.path.normpath(multi_img_folder_path)

        image_file_list = os.listdir(image_folder_path)
        image_file_list = sorted(image_file_list, key=utils.extract_number)
        img_file_len = len(image_file_list)

        video_file_list = os.listdir(video_folder_path)
        video_file_list = sorted(video_file_list, key=utils.extract_number)
        video_file_len = len(video_file_list)

        imageLink_file_list = os.listdir(imageLink_folder_path)
        imageLink_file_list = sorted(imageLink_file_list, key=utils.extract_number)
        imgLink_file_len = len(imageLink_file_list)

        multiimg_file_list = os.listdir(multi_img_folder_path)
        multiimg_file_list = sorted(multiimg_file_list, key=utils.extract_number)

        print(f"이미지 경로 : {image_folder_path}")
        print(f"이미지 파일들 : {image_file_list}")
        print(f"이미지 파일개수 : {img_file_len}")

        print()
        print(f"동영상 경로 : {video_folder_path}")
        print(f"동영상 파일들 : {video_file_list}")
        print(f"동영상 파일개수 : {video_file_len}")

        print()
        print(f"이미지링크 경로 : {imageLink_folder_path}")
        print(f"이미지링크 파일들 : {imageLink_file_list}")
        print(f"이미지링크 파일개수 : {imgLink_file_len}")

        print()
        print(f"멀티이미지 경로 : {multi_img_folder_path}")
        print(f"멀티이미지 폴더들 : {multiimg_file_list}")


        post_file_path = rf'{path}\자동업로드\{today_date}\원고\{p_title}.txt'
        post_file_path = os.path.normpath(post_file_path)  # 동영상 경로 표준화

        video_Link_folder_path = rf'{path}\자동업로드\{today_date}\영상 링크\{p_title}.txt'
        video_Link_folder_path = os.path.normpath(video_Link_folder_path)  # 원고 경로 표준화
        print()
        print(f"영상 링크 경로 : {video_Link_folder_path}")

        print()
        print(f"포스팅 원고파일 경로 : {post_file_path}")

        # 파일 읽기
        with open(post_file_path, 'r', encoding='utf-8') as file:
            file.seek(0)  # 파일 포인터를 파일의 처음으로 이동 (첫줄이 빈문자열로 나오는걸 방지하기 위함)
            post_title = file.readline().strip() # 제목
            original_post = file.read() # 본문
        print(post_title)

        # 영상링크 파일 불러오기
        with open(video_Link_folder_path, 'r') as file:
            videoLink_box = [line.strip() for line in file]
        print(videoLink_box)

        # mvpn 접속
        try:
            print("1")
            dlg = vpn_utils.mvpn_connect(downloaders.new_model, vpn_id, vpn_pw)
        except Exception as e:
            print(e)
            input("mvpn 접속 에러... 현재상태 캡쳐 부탁드리고, 터미널창에 엔터 입력후 ui가 종료되는지 체크 부탁드립니다.")
        time.sleep(5)

        # ### 네이버 로그인
        # try:
        #     headless_checked = False
        #     try:
        #         driver = driver_utils.driversetting(headless_checked)
        #         print("driver 세팅 완료")
        #     except:
        #         print("☆ Error driver setting...")
        #         print("30초후 재개 됩니다.")
        #         time.sleep(30)
        #         driver = driver_utils.driversetting(headless_checked)
        #
        #     driver.maximize_window()
        #     wait = WebDriverWait(driver, 10)
        #     try:
        #         driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #     except:
        #         print("□ 드라이버 오픈 에러.. 30초후 재시작합니다.")
        #         time.sleep(30)
        #         try:
        #             driver.close()
        #             time.sleep(5)
        #             driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #         except:
        #             driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #     time.sleep(1)
        #     wait, driver = driver_utils.naver_login(driver, wait, naver_id, naver_pw)  # 로그인 함수
        #
        #     # 블로그 클릭
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'service_icon.type_blog'))).click()
        #     time.sleep(1)
        #     # 글쓰기 클릭
        #     driver.switch_to.window(driver.window_handles[-1])
        #     wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
        #     time.sleep(3)
        #
        #     driver.switch_to.window(driver.window_handles[-1])
        #     driver.switch_to.default_content()  # 기본 iframe으로 복귀
        #     driver.switch_to.frame('mainFrame')
        # except:
        #     try:
        #         driver_utils.driver_close(driver)
        #     except:
        #         pass
        #
        #     headless_checked = False
        #     try:
        #         driver = driver_utils.driversetting(headless_checked)
        #         print("driver 세팅 완료")
        #     except:
        #         print("☆ Error driver setting...")
        #         print("30초후 재개 됩니다.")
        #         time.sleep(30)
        #         driver = driver_utils.driversetting(headless_checked)
        #
        #     driver.maximize_window()
        #     wait = WebDriverWait(driver, 10)
        #     try:
        #         driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #     except:
        #         print("□ 드라이버 오픈 에러.. 30초후 재시작합니다.")
        #         time.sleep(30)
        #         try:
        #             driver.close()
        #             time.sleep(5)
        #             driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #         except:
        #             driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
        #     time.sleep(1)
        #     wait, driver = driver_utils.naver_login(driver, wait, naver_id, naver_pw)  # 로그인 함수
        #
        #     # 블로그 클릭
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'service_icon.type_blog'))).click()
        #     time.sleep(1)
        #     # 글쓰기 클릭
        #     driver.switch_to.window(driver.window_handles[-1])
        #     wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
        #     time.sleep(3)
        #
        #     driver.switch_to.window(driver.window_handles[-1])
        #     driver.switch_to.default_content()  # 기본 iframe으로 복귀
        #     driver.switch_to.frame('mainFrame')
        #
        # # 작성 중인 글이 있습니다
        # time.sleep(5)
        # try:
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-popup-button-text"))).click()
        #     time.sleep(3)
        # except:
        #     print("popup_exception")
        #
        #
        # # 복붙용 크롬창 열기 (실제로는 여기에 작성)
        # driver.switch_to.window(driver.window_handles[-2])
        # wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='글쓰기']"))).click()
        # time.sleep(3)
        #
        #
        # # 글쓰기 시작
        # driver.switch_to.window(driver.window_handles[-2])
        # time.sleep(1)
        # driver.switch_to.default_content()  # 기본 iframe으로 복귀
        # driver.switch_to.frame('mainFrame')
        #
        # # 작성 중인 글이 있습니다
        # time.sleep(5)
        # try:
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-popup-button-text"))).click()
        #     time.sleep(3)
        # except:
        #     print("popup_exception")
        #
        # # 도움말 있는지 체크
        # # 도움말이 있으면 발행버튼이 안눌림
        # if 'se-help-panel-close-button' in str(driver.page_source):
        #     print('있다')
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-help-panel-close-button"))).click()
        #
        #
        # # 중요!!!! 브라우저 패널의 높이값
        # panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
        #
        # ### 제목 입력
        # # 제목 입력 element
        # # titel_input_box = driver.find_element(By.XPATH, """//span[text()='제목']""")
        # titel_input_box = wait.until(EC.presence_of_element_located((By.XPATH, """//span[text()='제목']""")))
        # # 제목 입력 element의 x 값 가져오기 (절대값)
        # abs_x = titel_input_box.location['x']
        # # 제목 입력 element의 y 값 가져오기 (상대값, 브라우저에 있는 y값)
        # y = titel_input_box.location['y']
        # abs_y = y + panel_height
        # # 마우스 이동해서 클릭
        # pyautogui.click(abs_x + 20, abs_y + 20)
        # time.sleep(1)
        # posting_utils.posting_run(post_title, image_folder_path, img_file_len, video_folder_path, video_file_len,
        #             imageLink_folder_path, imgLink_file_len, image_file_list, video_file_list, imageLink_file_list, videoLink_box, multi_img_folder_path, driver, wait, post_title, p_title)
        # time.sleep(3)
        #
        # ### 본문 입력
        # # 본문 입력 element
        # pyautogui.press('hangul')
        # contents_input_box = driver.find_element(By.CLASS_NAME,"se-canvas-bottom")
        # # 본문 입력 element
        # panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
        # # 본문 입력 element의 x 값 가져오기 (절대값)
        # abs_x = contents_input_box.location['x']
        # # 본문 입력 element의 y 값 가져오기 (상대값, 브라우저에 있는 y값)
        # y = contents_input_box.location['y']
        # abs_y = y + panel_height
        # pyautogui.click(abs_x + 1000, abs_y + 200)
        # time.sleep(3)
        # posting_utils.posting_run(original_post, image_folder_path, img_file_len, video_folder_path, video_file_len,
        #                           imageLink_folder_path, imgLink_file_len, image_file_list, video_file_list, imageLink_file_list, videoLink_box, multi_img_folder_path, driver, wait, post_title, p_title)
        #
        # # 도움말 있는지 체크
        # # 도움말이 있으면 발행버튼이 안눌림
        # if 'se-help-panel-close-button' in str(driver.page_source):
        #     print('있다')
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se-help-panel-close-button"))).click()
        #
        # # 발행
        # driver.switch_to.window(driver.window_handles[-2])
        # time.sleep(1)
        # driver.switch_to.default_content()  # 기본 iframe으로 복귀
        # driver.switch_to.frame('mainFrame')
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "publish_btn__m9KHH"))).click()
        # time.sleep(3)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "confirm_btn__WEaBq"))).click()
        #
        # print("발행 완료")
        #
        # time.sleep(3)
        # for _ in range(len(driver.window_handles)):
        #     driver.switch_to.window(driver.window_handles[-1])
        #     driver.close()
        #     time.sleep(0.5)
        # time.sleep(3)

        vpn_utils.mvpn_close(dlg)


        # try:
        #     vpn_utils.mvpn_close(dlg)
        # except:
        #     input("mvpn 종료 에러... 현재상태 캡쳐 부탁드리고, 터미널창에 엔터 입력후 ui가 종료되는지 체크 부탁드립니다.")
        time.sleep(3)

        minutes, seconds = utils.get_lab_time(start_time)
        print(f"■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")
        downloaders.new_model.textBrowser.append(f"■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")
        logger.debug(f"{p_title}- ■ [{number}] {post_title} 포스팅 완료.  소요시간 : {minutes}분 {seconds}초")

    success_data_list = utils.get_log_data_for_success()
    success_data_list = list(set(success_data_list))
    # 모든 p_title이 완료되었는지 확인
    print(len(success_data_list))
    print(len(df))
    if len(success_data_list) == len(df):
        print(f"■ 포스팅 모두 완료.")
        break  # 모든 p_title이 완료되면 while 문 종료

