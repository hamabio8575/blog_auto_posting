from moduls import *

def effect_reset(driver):
    html = BeautifulSoup(driver.page_source, 'lxml')
    if '굵기 해제' in str(html):
        pyautogui.hotkey('ctrl', 'b')
        time.sleep(1)
    elif '밑줄 해제' in str(html):
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(1)

def posting_effect(posting):
    # '①'와 'ⓟ' 사이의 문자열을 추출하는 정규 표현식
    inyoungu_box = re.compile(r'①(.*?)ⓟ').findall(posting)
    bold_box = re.compile(r'②(.*?)ⓑ').findall(posting)
    underline_box = re.compile(r'③(.*?)ⓤ').findall(posting)
    # breakline_box = re.compile(r'④(.*?)ⓗ').findall(posting)
    return inyoungu_box, bold_box, underline_box


def is_numlock_on():
    VK_NUMLOCK = 0x90  # Num Lock 키의 가상 키 코드
    hllDll = ctypes.WinDLL("User32.dll")
    numlock_checked = hllDll.GetKeyState(VK_NUMLOCK) & 0x0001 != 0
    if numlock_checked:
        print("Num lock이 On 입니다.. Num lock을 Off 하겠습니다.")
        pyautogui.press('numlock')
    else:
        print("Num lock이 Off 입니다")


def posting_run(write_contents, image_folder_path, img_file_len, video_folder_path, video_file_len, imageLink_folder_path, imgLink_file_len, image_file_list, video_file_list, imageLink_file_list, videoLink_box, multi_img_folder_path, driver, wait, post_title, p_title):
    from string import ascii_lowercase, ascii_uppercase
    import time, pyautogui

    pyautogui.FAILSAFE = False

    little_alpha_list = list(ascii_lowercase)
    big_alpha_list = list(ascii_uppercase)

    posting = write_contents
    # posting = '안녕하세요\n제이름은\n윤성노 입니다.\n나이는 39세이고\n대한민국 사람입니다.\n잘부탁드립니다.\n'
    posting = posting.replace("\xa0", " ")
    posting = posting.replace("  ", " ").replace("\n", "\n ")

    # 한글 초성, 중성, 종성 리스트 정의
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                     'ㅣ']
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                     'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    # 한글 글자를 영어로 변환하는 함수 정의
    def korean_to_be_englished(korean_word):
        r_lst = []
        for w in list(korean_word.strip()):
            if '가' <= w <= '힣':
                ch1 = (ord(w) - ord('가')) // 588
                ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
                ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
                r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
            else:
                r_lst.append([w])
        return r_lst

    inyoungu_box, bold_box, underline_box = posting_effect(posting)
    print(inyoungu_box, bold_box, underline_box)

    # 포스팅 내용을 한글 음절 단위로 변환하여 리스트로 반환
    post_list = korean_to_be_englished(posting)

    # 변환된 리스트를 하나의 리스트로 합침
    result_list = []
    for l in post_list:
        result_list += l



    # 한글 음절을 영어로 변환하는 딕셔너리 정의
    cons_reverse = {
        'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
        'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ', 'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ',
        'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ', 'ho': 'ㅙ', 'hl': 'ㅚ',
        'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ', 'rt': 'ㄳ',
        'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ', 'fg': 'ㅀ', 'qt': 'ㅄ',
        ' ': ' ', '!': '!', '\n': '\n',
        '@': '@', '#': '#', '$': '$', '%': '%', '^': '^', '&': '&', '*': '*', '(': '(', ')': ')', '_': '_', '+': '+',
        '-': '-', '=': '=', '~': '~', '`': '`', '{': '{', '}': '}', '[': '[', ']': ']', ';': ';', ':': ':', '"': '"',
        "'": "'", '<': '<', ',': ',', '>': '>', '.': '.', '?': '?', '/': '/',
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
        '①': '①', 'ⓟ': 'ⓟ', '②': '②', 'ⓑ': 'ⓑ', '③': '③', 'ⓤ': 'ⓤ', '④': '④', 'ⓗ': 'ⓗ', '⑤': '⑤', 'ⓥ': 'ⓥ'
    }

    # 영어를 한글 음절로 변환하는 딕셔너리 생성
    cons = {v: k for k, v in cons_reverse.items()}

    # 영문으로 변환된 리스트 생성
    eng_post_list = []
    for l in result_list:
        for key, value in cons.items():
            if l == key:
                eng_post_list.append(value)
            elif l in little_alpha_list:
                eng_post_list.append(l)
                break
            elif l in big_alpha_list:
                eng_post_list.append(l)
                break

    # result_list에 있는 모든 문자열을 하나의 문자열로 합침
    joined_string = "".join(result_list)

    # 공백을 기준으로 문자열을 분리하여 리스트로 만듦
    split_strings = joined_string.split(" ")

    # 분리된 문자열들을 순회하면서 인덱스와 함께 반복
    alpha_index = []
    for ri, rl in enumerate(split_strings):
        if len(rl) != 0:
            if rl[0] == " ":
                alpha_index.append(ri)
            elif rl[0] in little_alpha_list or rl[0] in big_alpha_list:
                alpha_index.append(ri)
            elif rl[0] == '(':
                if len(rl) == 1:
                    pass
                else:
                    if rl[1] in little_alpha_list or rl[1] in big_alpha_list:
                        alpha_index.append(ri)

    # 최종적으로 영문으로 변환된 리스트를 담을 리스트 생성
    final_eng_list = "".join(eng_post_list).split(" ")
    final_eng_list_box = [f + " " for f in final_eng_list]

    # 한글 입력 모드로 변경
    pyautogui.press('hangul')

    multiimg_file_list = os.listdir(multi_img_folder_path)

    # 이미지 파일 카운트 변수 초기화
    img_cnt = 0
    video_cnt = 0
    img_link_cnt = 0
    videolink_cnt = 0
    multi_img_cnt = 0


    inyoungu_cnt = 0
    bold_cnt = 0
    underline_cnt = 0
    breaklinecnt = 0
    # 변환된 영문 리스트를 순회하면서 입력 작업 수행
    for ei, eng_list1 in enumerate(final_eng_list_box):
        eng_list1 = eng_list1.replace("\n ", "\n")
        for ii, e in enumerate(eng_list1):
            if ei in alpha_index:
                pyautogui.press('hangul')
                pyautogui.press(e)
                pyautogui.press('hangul')
            else:
                if e == '$':  # 이미지
                    img_cnt += 1
                    if img_cnt > img_file_len:
                        pass
                    else:
                        image_file_path = rf"{image_folder_path}\{image_file_list[img_cnt-1]}"

                        #                 print("●"*30)

                        # 기본창으로 이동
                        driver.switch_to.window(driver.window_handles[-2])
                        driver.switch_to.default_content()  # 기본 iframe으로 복귀
                        driver.switch_to.frame('mainFrame')

                        # 사진 아이콘 클릭
                        # driver.find_element(By.CLASS_NAME,
                        #                     'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry').click()
                        # wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                        #                                             "se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry"
                        #                                             ))).click()
                        pyautogui.hotkey('ctrl', 'alt', 'i')
                        time.sleep(2)

                        try:
                            autoit.control_focus("열기", "")
                            time.sleep(1)
                            autoit.control_set_text("열기", "Edit1", image_file_path)
                            time.sleep(1)
                            autoit.control_click("열기", "Button1")
                            time.sleep(1)
                        except:
                            time.sleep(10)
                            pyautogui.hotkey('ctrl', 'alt', 'i')
                            time.sleep(2)

                            autoit.control_focus("열기", "")
                            time.sleep(1)
                            autoit.control_set_text("열기", "Edit1", image_file_path)
                            time.sleep(1)
                            autoit.control_click("열기", "Button1")
                            time.sleep(1)

                        while True:
                            if '전송중' in wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text:
                                print(f"이미지 ({img_cnt}).jpg 업로드중...")
                                time.sleep(3)
                            else:
                                print(f"이미지 ({img_cnt}).jpg 업로드 완료")
                                break
                            time.sleep(3)
                            if '파일 전송 오류' in driver.find_element(By.TAG_NAME, 'body').text:
                                print('파일 전송 오류')
                                driver.find_element(By.CLASS_NAME, "se-popup-button.se-popup-button-confirm").click()
                                break
                elif e == '@':  # 이미지 링크(라이브러리 제외)
                    img_link_cnt += 1
                    if img_link_cnt > imgLink_file_len:
                        pass
                    else:
                        imageLink_file_path = rf"{imageLink_folder_path}\{imageLink_file_list[img_link_cnt-1]}"

                        # 샘플 복붙용창으로 이동
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.switch_to.default_content()  # 기본 iframe으로 복귀
                        driver.switch_to.frame('mainFrame')

                        # 사진 아이콘 클릭
                        # driver.find_element(By.CLASS_NAME,
                        #                     'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry').click()
                        time.sleep(2)
                        pyautogui.hotkey('ctrl', 'alt', 'i')
                        time.sleep(2)

                        try:
                            autoit.control_focus("열기", "")
                            time.sleep(1)
                            autoit.control_set_text("열기", "Edit1", imageLink_file_path)
                            time.sleep(1)
                            autoit.control_click("열기", "Button1")
                            time.sleep(1)
                        except:
                            time.sleep(10)
                            pyautogui.hotkey('ctrl', 'alt', 'i')
                            time.sleep(2)

                            autoit.control_focus("열기", "")
                            time.sleep(1)
                            autoit.control_set_text("열기", "Edit1", imageLink_file_path)
                            time.sleep(1)
                            autoit.control_click("열기", "Button1")
                            time.sleep(1)

                        while True:
                            if '전송중' in wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text:
                                print(f"이미지링크 ({img_link_cnt}).jpg 업로드중...")
                                time.sleep(3)
                            else:
                                print(f"이미지링크 ({img_link_cnt}).jpg 업로드 완료")
                                break
                            time.sleep(3)
                            if '파일 전송 오류' in driver.find_element(By.TAG_NAME, 'body').text:
                                print('파일 전송 오류')
                                driver.find_element(By.CLASS_NAME, "se-popup-button.se-popup-button-confirm").click()
                                break

                        ### 업로드한 이미지 찾아서 복사

                        # 이미지 업로드후 젤 위로 이동
                        time.sleep(1)
                        for _ in range(10):
                            pyautogui.press("up")
                        time.sleep(3)

                        panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
                        # 이미지 element
                        try:
                            posting_image = driver.find_elements(By.TAG_NAME, 'section')[0].find_element(By.TAG_NAME, 'img')
                        except Exception as e:
                            print(e)
                            time.sleep(5)
                            posting_image = driver.find_elements(By.TAG_NAME, 'section')[0].find_element(By.TAG_NAME,
                                                                                                         'img')
                        # 제목 입력 element의 x 값 가져오기 (절대값)
                        abs_x = posting_image.location['x'] + 200
                        # 제목 입력 element의 y 값 가져오기 (상대값, 브라우저에 있는 y값)
                        y = posting_image.location['y']
                        abs_y = y + panel_height + 200
                        # 마우스 이동해서 클릭
                        pyautogui.moveTo(abs_x, abs_y)
                        time.sleep(3)
                        pyautogui.click()
                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'c')
                        time.sleep(1)
                        for _ in range(3):
                            pyautogui.press('delete')
                            time.sleep(1)

                        # 원본창 으로 이동
                        driver.switch_to.window(driver.window_handles[-2])
                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(1)

                elif e == '&':  # 동영상
                    video_cnt += 1
                    if video_cnt > video_file_len:
                        pass
                    else:
                        video_file_path = rf"{video_folder_path}\{video_file_list[video_cnt-1]}"

                        # 원본창으로 이동
                        driver.switch_to.window(driver.window_handles[-2])
                        driver.switch_to.default_content()  # 기본 iframe으로 복귀
                        driver.switch_to.frame('mainFrame')

                        # 동영상 클릭
                        # wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='동영상']"))).click()
                        # pyautogui.hotkey('ctrl', 'alt', 'm')
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-name='video']"))).click()
                            time.sleep(3)
                            # 동영상 추가 클릭
                            wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, "nvu_btn_append.nvu_local"))).click()
                            time.sleep(3)
                        except Exception as e:
                            print(e)
                            time.sleep(10)
                            wait.until(
                                EC.presence_of_element_located((By.XPATH, "//button[@data-name='video']"))).click()
                            time.sleep(3)
                            # 동영상 추가 클릭
                            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_btn_append.nvu_local"))).click()
                            time.sleep(3)

                        # 영상파일 선택
                        autoit.control_focus("열기", "")
                        time.sleep(1)
                        autoit.control_set_text("열기", "Edit1", video_file_path)
                        time.sleep(1)
                        autoit.control_click("열기", "Button1")
                        time.sleep(1)

                        while True:
                            if '로딩중' in wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text:
                                print(f"영상 ({video_cnt}).mp4 업로드중....")
                                time.sleep(3)
                            else:
                                # 제목
                                wait.until(EC.presence_of_element_located((By.ID, "nvu_inp_box_title"))).send_keys(
                                    post_title)
                                # 정보
                                wait.until(
                                    EC.presence_of_element_located((By.ID, "nvu_inp_box_description"))).send_keys(
                                    p_title)
                                # 태그추가 클릭
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_tag_label"))).click()
                                # 태그 입력
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_tag_inp"))).send_keys(
                                    p_title.replace(" ", ""))
                                wait.until(EC.presence_of_element_located(
                                    (By.CLASS_NAME, "nvu_btn_submit.nvu_btn_type2"))).click()
                                print(f"영상 ({video_cnt}).mp4 업로드 완료")
                                time.sleep(3)
                                break
                            time.sleep(3)
                            if '파일 전송 오류' in driver.find_element(By.TAG_NAME, 'body').text:
                                print('파일 전송 오류')
                                driver.find_element(By.CLASS_NAME, "se-popup-button.se-popup-button-confirm").click()
                                break

                elif e == '%':  # 구분선
                    pyautogui.hotkey('ctrl', 'alt', 'h')


                # 동영상 링크
                elif e == '④':
                    try:
                        pyperclip.copy(videoLink_box[videolink_cnt])
                    except:
                        continue
                    pyautogui.hotkey('ctrl', 'v')
                    videolink_cnt += 1
                    time.sleep(10)

                # 멀티이미지(슬라이드)
                elif e == '⑤':
                    multi_img_cnt += 1
                    if multi_img_cnt > len(multiimg_file_list):
                        continue

                    driver.switch_to.window(driver.window_handles[-2])
                    driver.switch_to.default_content()  # 기본 iframe으로 복귀
                    driver.switch_to.frame('mainFrame')
                    time.sleep(3)

                    # driver.find_element(By.CLASS_NAME,
                    #                     'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry').click()
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                               "se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry"))).click()
                    time.sleep(3)

                    # 웹상의 사진 업로드 버튼을 클릭후 파일탐색창이 정상적으로 업로드 되었는지 체크
                    try:
                        autoit.win_wait_active("열기", 5)
                        print("팝업완료")
                    except autoit.AutoItError:
                        # 파일 탐색창이 업로드 되지 않았다면 사진 업로드 버튼 다시 클릭
                        print("팝업X - 타임아웃 발생, 재시도...")
                        time.sleep(5)
                        # driver.find_element(By.CLASS_NAME,
                        #                     'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry').click()
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                   "se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry"))).click()
                        print("팝업완료")
                    time.sleep(3)

                    # 파일 탐색창을 선택
                    # "열기"는 파일탐색창 좌측 상단에 있는 title명
                    autoit.win_activate("열기")
                    multi_img_folder_path_cnt =rf"{multi_img_folder_path}\{multi_img_cnt}"

                    # 파일 탐색창에 선택하고자 하는 파일의 경로 입력후 엔터
                    autoit.control_set_text("열기", "Edit1", multi_img_folder_path_cnt)
                    time.sleep(1)
                    autoit.send("{ENTER}")
                    time.sleep(1)

                    # 파일 탐색창을 선택
                    autoit.win_activate("열기")

                    # 파일 탐색창의 파일을 선택할수 있는 영역을 선택
                    autoit.control_focus("열기", "DirectUIHWND2")
                    # 파일 전체 선택후 엔터
                    autoit.send("^a")  # 'Ctrl + A'로 전체 파일 선택
                    time.sleep(1)
                    autoit.send("{ENTER}")
                    time.sleep(3)

                    # 파일선택후 열기버튼을 클릭한후 탐색창이 정상적으로 닫혔는지 구분
                    # 안닫혔으면 닫힐때까지 시도
                    while autoit.win_exists("열기"):
                        print("??")
                        # 파일 탐색창을 선택
                        autoit.win_activate("열기")
                        # 파일 탐색창의 파일을 선택할수 있는 영역을 선택
                        autoit.control_focus("열기", "DirectUIHWND2")
                        # 파일 전체 선택후 엔터
                        autoit.send("^a")  # 'Ctrl + A'로 전체 파일 선택
                        time.sleep(1)
                        autoit.send("{ENTER}")
                        time.sleep(2)

                    # 멀티이미지 슬라이드 방식 선택
                    wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='image-type-slide']"))).click()
                    while True:
                        if '전송중' in wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text:
                            print(f"멀티이미지 ({multi_img_cnt}폴더) 업로드중...")
                            time.sleep(3)
                        else:
                            print(f"멀티이미지 ({multi_img_cnt}폴더) 업로 완료")
                            break

                        time.sleep(3)
                        if '파일 전송 오류' in driver.find_element(By.TAG_NAME, 'body').text:
                            print('파일 전송 오류')
                            driver.find_element(By.CLASS_NAME, "se-popup-button.se-popup-button-confirm").click()
                            break
                    time.sleep(3)

                else:
                    # 인용구 시작이면 인용구 삽입
                    if e == '①':
                        is_numlock_on()
                        pyautogui.hotkey('ctrl', 'alt', 'q')
                        time.sleep(3)

                    # 인용구 종료이면 커서 내리기
                    elif e == 'ⓟ':
                        is_numlock_on()
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(1)
                        pyautogui.press('down')
                        time.sleep(1)
                        pyautogui.press('down')
                        time.sleep(1)
                        pyperclip.copy(" ")
                        pyautogui.hotkey('ctrl', 'v')
                        pyautogui.press('backspace')

                    # 볼드체
                    elif e == 'ⓑ':
                        is_numlock_on()
                        try:
                            p_len = len(bold_box[bold_cnt])
                        except:
                            print("볼드체 적용과정에서 문제가 발생했습니다. 원고에서 '②'또는 'ⓑ'가 제대로 입력되었는지 확인부탁드립니다.")
                            continue
                        for _ in range(p_len):
                            pyautogui.hotkey('shift', 'left')

                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'b')
                        time.sleep(1)
                        pyautogui.press('end')
                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'b')
                        time.sleep(1)
                        bold_cnt += 1

                    # 밑줄
                    elif e == 'ⓤ':
                        is_numlock_on()
                        try:
                            p_len = len(underline_box[underline_cnt])
                        except:
                            print("밑줄 적용과정에서 문제가 발생했습니다. 원고에서 '③'또는 'ⓤ'가 제대로 입력되었는지 확인부탁드립니다.")
                            continue
                        for _ in range(p_len):
                            pyautogui.hotkey('shift', 'left')

                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'u')
                        time.sleep(1)
                        pyautogui.press('end')
                        time.sleep(1)
                        pyautogui.hotkey('ctrl', 'u')
                        time.sleep(1)
                        underline_cnt += 1
                    else:
                        effect_reset(driver)
                        pyautogui.press(e)