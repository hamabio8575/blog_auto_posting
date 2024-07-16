from moduls import *

def posting_run(write_contents, image_folder_path, img_file_len, video_folder_path, video_file_len, driver, wait, post_title, p_title):
    from string import ascii_lowercase, ascii_uppercase
    import time, pyautogui

    pyautogui.FAILSAFE = False

    little_alpha_list = list(ascii_lowercase)
    big_alpha_list = list(ascii_uppercase)

    posting = write_contents
    # posting = '안녕하세요\n제이름은\n윤성노 입니다.\n나이는 39세이고\n대한민국 사람입니다.\n잘부탁드립니다.\n'
    posting= posting.replace("  ", " ").replace("\n", "\n ")

    # 초성 리스트. 00 ~ 18
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    # 중성 리스트. 00 ~ 20
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    double_list = ['ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ', 'ㄳ','ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ','ㅄ']

    def korean_to_be_englished(korean_word):
        r_lst = []
        for w in list(korean_word.strip()):
            ## 영어인 경우 구분해서 작성함.
            if '가'<=w<='힣':
                ## 588개 마다 초성이 바뀜.
                ch1 = (ord(w) - ord('가'))//588
                ## 중성은 총 28가지 종류
                ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
                ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
                r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
            else:
                r_lst.append([w])
        return r_lst

    post_list = korean_to_be_englished(posting)
    result_list =[]
    for l in post_list:
        result_list += l
    result_list


    cons_reverse = {
        'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
        'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ', 'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
        'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ','rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ',
        ' ':' ', '!': '!','\n':'\n',
         '@': '@',
         '#': '#',
         '$': '$',
         '%': '%',
         '^': '^',
         '&': '&',
         '*': '*',
         '(': '(',
         ')': ')',
         '_': '_',
         '+': '+',
         '-': '-',
         '=': '=',
         '~': '~',
         '`': '`',
         '{': '{',
         '}': '}',
         '[': '[',
         ']': ']',
         ';': ';',
         ':': ':',
         '"': '"',
         "'": "'",
         '<': '<',
         ',': ',',
         '>': '>',
         '.': '.',
         '?': '?',
         '/': '/',
         '1':'1',
         '2':'2',
         '3':'3',
         '4':'4',
         '5':'5',
         '6':'6',
         '7':'7',
         '8':'8',
         '9':'9',
         '0':'0',
           }
    cons = {v:k for k,v in cons_reverse.items()}



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

    alpha_index = []
    # 분리된 문자열들을 순회하면서 인덱스와 함께 반복
    for ri, rl in enumerate("".join(result_list).split(" ")):
        if len(rl) != 0:
            if rl[0] == " ":
                alpha_index.append(ri)
            elif rl[0] in little_alpha_list or rl[0] in big_alpha_list:
                alpha_index.append(ri)
            elif rl[0] == '(':
                if rl[1] in little_alpha_list or rl[1] in big_alpha_list:
                    alpha_index.append(ri)

    time.sleep(3)
    final_eng_list = "".join(eng_post_list).split(" ")
    final_eng_list_box = []
    for f in final_eng_list:
        final_eng_list_box.append(f+" ")
    pyautogui.press('hangul')

    img_cnt = 0
    video_cnt = 0
    for ei, eng_list1 in enumerate(final_eng_list_box):
        eng_list1 = eng_list1.replace("\n ","\n")
        for ii, e in enumerate(eng_list1):
            if ei in alpha_index:
                pyautogui.press('hangul')
                pyautogui.press(e)
                pyautogui.press('hangul')
            else:
                if e == '$':
                    img_cnt += 1
                    if img_cnt > img_file_len:
                        pass
                    else:
                        image_file_path = rf"{image_folder_path}\이미지 ({img_cnt}).jpg"

            #                 print("●"*30)
                        # 사진 아이콘 클릭
                        driver.find_element(By.CLASS_NAME, 'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button.__se-sentry').click()
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

                elif e == '&':

                    video_cnt += 1
                    if video_cnt > video_file_len:
                        pass
                    else:
                        video_file_path = rf"{video_folder_path}\영상 ({video_cnt}).mp4"

                        # 동영상 클릭
                        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='동영상']"))).click()
                        # 동영상 추가 클릭
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_btn_append.nvu_local"))).click()
                        time.sleep(2)

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
                                # 태크추가 클릭
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_tag_label"))).click()
                                # 태크 입력
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nvu_tag_inp"))).send_keys(
                                    p_title.replace(" ", ""))
                                wait.until(EC.presence_of_element_located(
                                    (By.CLASS_NAME, "nvu_btn_submit.nvu_btn_type2"))).click()
                                print(f"영상 ({video_cnt}).mp4 업로드 완료")
                                break
                else:
                    pyautogui.press(e)