from moduls import *

global new_paht

### 주소 저장된 파일 선택 함수
def file_button(model):

    current_directory = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 파일의 경로
    path = QFileDialog.getExistingDirectory(model, '폴더 선택', current_directory)

    global new_paht
    new_paht = path

    model.textBrowser.append(f"선택 폴더 -- {path}\n")