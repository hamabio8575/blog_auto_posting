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


# 소요시간 계산산
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


