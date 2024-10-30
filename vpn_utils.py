from moduls import *
import driver_utils


# mvpn 로그인및 접속
def mvpn_connect(model, mvpn_id, mvpn_pw):
    # 현재 윈도우 화면에 있는 프로세스 목록 리스트를 반환한다.
    # 리스트의 각 요소는 element 객체로 프로세스 id, 핸들값, 이름 등의 정보를 보유한다.
    # procs = findwindows.find_elements()
    # for proc in procs:
    #     print(f"{proc} / 프로세스 : {proc.process_id}")
    print(f"■VPN 접속시도({mvpn_id})")
    model.textBrowser.append(f"■ VPN 접속시도({mvpn_id})")
    app = application.Application(backend='uia')

    # 프로세스의 경로를 넣어 실행해준다.
    app.start(r"C:\Program Files (x86)\mvpn\mvpn.exe")

    dlg = app['mvpn']  # 변수에 mvpn 윈도우 어플리케이션 객체를 할당
    # dlg.print_control_identifiers()  #속성값들 확인
    time.sleep(3)

    # 메모 입력 (띄어쓰기 하려면 반드시 with_spaces=True
    dlg['Edit1'].type_keys("", with_spaces=True)
    dlg['Edit2'].type_keys(mvpn_pw, with_spaces=True)
    dlg['Edit1'].type_keys(mvpn_id, with_spaces=True)
    time.sleep(1)
    dlg['Button'].click()
    time.sleep(3)

    # 로그인후 다시 윈도우 어플리케이션 객체 할당
    app.connect(title="Dialog")  # 로그인후 프로그램명(Dialog)으로 연결
    dlg = app['Dialog']  # 변수에 mvpn 윈도우 어플리케이션 객체를 할당
    time.sleep(3)
    dlg['Button3'].click()  # 접속하기 버튼
    print('■접속하기 버튼 클릭, 접속 대기중...')

    while True:
        if dlg['Static4'].window_text() == '접속완료':
            print('■접속 완료')
            model.textBrowser.append(f"■접속 완료({mvpn_id})")
            time.sleep(1)
            break
        elif '오류' in dlg['Static4'].window_text():
            model.textBrowser.append(f"□ {dlg['Static4'].window_text()}")
            model.textBrowser.append(f"□ 수동으로 mvpn접속후 커맨드창에 아무키나 입력후 엔터를 눌러주세요.")

            print(f"□ {dlg['Static4'].window_text()}")
            print(f"□ 수동으로 mvpn접속후 커맨드창에 아무키나 입력후 엔터를 눌러주세요.")
            input()
            time.sleep(1)
            break
        else:
            time.sleep(1)
    return dlg


# mpv 닫기
def mvpn_close(dlg):
    dlg['Button6'].click()  # 닫기 버튼 클릭
    time.sleep(2)
    dlg['Button'].click()  # Alert창 예 버튼 클릭
    time.sleep(1)
    print("mvpn 종료")
    time.sleep(1)


def ip_checked(model, ip):
    headless_checked = True
    ip_check_driver = driver_utils.driversetting(headless_checked)
    ip_check_driver.get("https://ip.pe.kr/")
    ip_checkd = ip_check_driver.find_element(By.CLASS_NAME, "cover-heading").text
    if ip_checkd == ip:
        print(f"■아이피( {ip} ) 일치")
        model.textBrowser.append(f"■아이피( {ip} ) 일치")
        ip_check_driver.quit()
    else:
        print("불일치.... 일경우 어떻게 해야 할까....")