from moduls import *



# 한/영 체크
def ko_eng_checked():
    while True:
        ko_eng_check_input = input("문자열을 입력하세요: ")
        # 입력된 문자열이 모두 한글인지 확인
        if all(('가' <= char <= '힣' or 'ㄱ' <= char <= 'ㅣ') for char in ko_eng_check_input):
            print("□입력된 문자열은 한글입니다. 영문으로 변경후 다시 체크해주세요.")
        elif ko_eng_check_input.isalpha() and all(
                'a' <= char <= 'z' or 'A' <= char <= 'Z' for char in ko_eng_check_input):
            print("■입력된 문자열은 영어입니다. 계속해서 프로그램을 진행하겠습니다.")
            break
        else:
            print("□입력된 문자열은 혼합 또는 다른 문자입니다.영문으로 변경후 다시 체크해주세요.")


def get_today_date():
    # 오늘 날짜 가져오기
    today = datetime.today()
    # 날짜를 원하는 형식으로 포맷팅
    formatted_date = today.strftime("%m월 %d일").lstrip("0").replace(" 0", " ")
    return formatted_date


# 소요시간 계산
def get_lab_time(start_time):
    end_time = time.time()  # 종료 시간 기록
    # 총 소요 시간 계산
    total_time = end_time - start_time
    # 분과 초로 변환
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    return minutes, seconds


# 로그 설정
def setup_logging():
    current_time = datetime.today()
    logfilename = f"{current_time.strftime('%Y%m%d')} 로그.log"

    # 로거 생성
    logger = logging.getLogger('블로그 자동업로드')
    logger.setLevel(logging.DEBUG)

    # 기존 핸들러 제거
    if logger.hasHandlers():
        logger.handlers.clear()

    # 핸들러 생성 (파일 출력)
    file_handler = logging.FileHandler(logfilename)

    # 포매터 생성 및 핸들러에 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # 로거에 핸들러 추가
    logger.addHandler(file_handler)

    return logger, file_handler


def extract_number(file_name):
    # 정규표현식을 사용하여 괄호 안에 있는 숫자만 추출 (예: '이미지 (10).jpg'에서 10 추출)
    match = re.search(r'\((\d+)\)', file_name)
    if match:
        return int(match.group(1))
    return 0  # 숫자를 찾지 못하면 0을 반환 (필요시 다른 값을 반환하도록 수정 가능)


def file_size_check(path, model):
    ### 이미지 크기 체크

    today = datetime.today()
    today_date = get_today_date()  # 오늘 날짜 확인 // format : 5월24일
    df = pd.read_excel("블로그 포스팅 세팅 파일.xlsx")
    df = df.iloc[:, :7]

    image_over_size_list = []
    for number, naver_id, naver_pw, vpn_name, vpn_id, vpn_pw, p_title in df.to_numpy().tolist():
        print(p_title)
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

            imageLink_folder_path = os.path.join(
                path,
                "자동업로드",
                today_date,
                '이미지링크',
                p_title,
            )


            image_folder_path = os.path.normpath(image_folder_path)  # 이미지 경로 표준화

        image_file_list = os.listdir(image_folder_path)
        image_file_list = sorted(image_file_list, key=extract_number)
        img_file_len = len(image_file_list)

        for file_name in image_file_list:
            file_path = os.path.join(image_folder_path, file_name)
            file_size_bytes = os.path.getsize(file_path)  # 파일 크기를 바이트 단위로 가져옴

            # KB 계산 (소수점 첫째 자리에서 올림하여 정수로 변환)
            file_size_kb = file_size_bytes / 1024  # 킬로바이트로 변환
            file_size_kb_rounded = math.ceil(file_size_kb)  # 소수점 첫째 자리에서 올림하여 정수

            # MB 계산 (소수점 둘째 자리까지 출력)
            file_size_mb = file_size_bytes / (1024 * 1024)  # 메가바이트로 변환
            file_size_mb_rounded = round(file_size_mb, 2)  # 소수점 둘째 자리까지 반올림

            if file_size_mb_rounded > 20:
                image_over_size_list.append(f"{p_title} -- 이미지 '{file_name}' 제한사이즈 초과, {file_size_mb_rounded:.2f} MB")


    image_link_over_size_list = []
    for number, naver_id, naver_pw, vpn_name, vpn_id, vpn_pw, p_title in df.to_numpy().tolist():
        print(p_title)
        start_time = time.time()
        if path:
            # 이미지 링크 경로 생성
            imageLink_folder_path = os.path.join(
                path,
                "자동업로드",
                today_date,
                '이미지링크',
                p_title,
            )

            image_Link_folder_path = os.path.normpath(imageLink_folder_path)  # 이미지링크 경로 표준화

        imageLink_file_list = os.listdir(image_Link_folder_path)
        imageLink_file_list = sorted(imageLink_file_list, key=extract_number)
        imgLink_file_len = len(imageLink_file_list)

        for file_name in imageLink_file_list:
            file_path = os.path.join(image_Link_folder_path, file_name)
            file_size_bytes = os.path.getsize(file_path)  # 파일 크기를 바이트 단위로 가져옴

            # KB 계산 (소수점 첫째 자리에서 올림하여 정수로 변환)
            file_size_kb = file_size_bytes / 1024  # 킬로바이트로 변환
            file_size_kb_rounded = math.ceil(file_size_kb)  # 소수점 첫째 자리에서 올림하여 정수

            # MB 계산 (소수점 둘째 자리까지 출력)
            file_size_mb = file_size_bytes / (1024 * 1024)  # 메가바이트로 변환
            file_size_mb_rounded = round(file_size_mb, 2)  # 소수점 둘째 자리까지 반올림

            if file_size_mb_rounded > 20:
                image_link_over_size_list.append(f"{p_title} -- 이미지 링크 '{file_name}' 제한사이즈 초과, {file_size_mb_rounded:.2f} MB")



    video_over_size_list = []
    for number, naver_id, naver_pw, vpn_name, vpn_id, vpn_pw, p_title in df.to_numpy().tolist():
        start_time = time.time()
        if path:
            video_folder_path = os.path.join(
                path,
                "자동업로드",
                today_date,
                '영상',
                p_title,
            )
            video_folder_path = os.path.normpath(video_folder_path)  # 동영상 경로 표준화

        video_file_list = os.listdir(video_folder_path)
        video_file_list = sorted(video_file_list, key=extract_number)
        video_file_len = len(video_file_list)

        for file_name in video_file_list:
            file_path = os.path.join(video_folder_path, file_name)
            file_size_bytes = os.path.getsize(file_path)  # 파일 크기를 바이트 단위로 가져옴

            # KB 계산 (소수점 첫째 자리에서 올림하여 정수로 변환)
            file_size_kb = file_size_bytes / 1024  # 킬로바이트로 변환
            file_size_kb_rounded = math.ceil(file_size_kb)  # 소수점 첫째 자리에서 올림하여 정수

            # MB 계산 (소수점 둘째 자리까지 출력)
            file_size_mb = file_size_bytes / (1024 * 1024)  # 메가바이트로 변환
            file_size_mb_rounded = round(file_size_mb, 2)  # 소수점 둘째 자리까지 반올림

            if file_size_mb_rounded > 999:
                video_over_size_list.append(f"{p_title} -- 영상 '{file_name}' 제한사이즈 초과, {file_size_mb_rounded:.2f} MB")

    if len(image_over_size_list) > 0 or len(video_over_size_list) > 0 or len(image_link_over_size_list) > 0:
        print(image_over_size_list)
        print(image_link_over_size_list)
        print(video_over_size_list)
        print("용량 초과 파일이 발견되어서 프로그램 실행을 종료 합니다.")
        model.textBrowser.append("★ 용량 초과 파일이 발견되어서 프로그램 실행을 종료 합니다.")
        sys.exit()  # 프로그램을 종료합니다.



def get_log_data_for_success():
    """
    이어서 할수 있도록 오늘날짜 로그파일 받아와서 성공여부 확인하기
    :return: 성공한 포스팅 리스트
    """
    today = datetime.now().strftime("%Y%m%d")
    with open(f"{today} 로그.log", 'r') as log_file:
        lines = log_file.readlines()
        log_lines = [line.strip() for line in lines]  # Stripping newline characters for each line

        success_data_list = []
        for log_data in log_lines:
            success_data_list.append(log_data.split("-")[5].strip())
    return success_data_list