from moduls import *

global new_paht

### 주소 저장된 파일 선택 함수
def file_button(model):

    current_directory = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 파일의 경로
    path = QFileDialog.getExistingDirectory(model, '폴더 선택', current_directory)

    global new_paht
    new_paht = path

    model.textBrowser.append(f"선택 폴더 -- {path}\n")


def logfile_open(model):
    current_time = datetime.today()
    logfilename = f"{current_time.strftime('%Y%m%d')} 로그.log"
    try:
        os.startfile(logfilename)
    except:
        print(f"당일({current_time.strftime('%Y%m%d')})로그가 없습니다.")