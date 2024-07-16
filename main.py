from moduls import *
import apps
import password_check

#
# import crawling
# from crawling import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('blog_auto_posting.ui')
form_class = uic.loadUiType(form)[0]

# if getattr(sys, 'frozen', False):
#     # If the application is running as a PyInstaller bundle
#     application_path = sys._MEIPASS
# else:
#     application_path = os.path.dirname(os.path.abspath(__file__))
# autoit_path = os.path.join(application_path, 'autoit')
# sys.path.append(autoit_path)

# import autoit  # Now you can import autoit

class MyWindow(QtWidgets.QMainWindow, QMessageBox, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tab_2.setDisabled(True)
        self.pushButton_9.clicked.connect(self.password_check_btn)

        self.pushButton_2.clicked.connect(self.folder_select_button)
        self.pushButton_3.clicked.connect(self.start_button)
        # self.pushButton_3.clicked.connect(self.file_button)

    def password_check_btn(self):
        qqq = threading.Thread(target=password_check.password_check_run, args=(model,))
        qqq.start()

    def folder_select_button(self):
        qqq = threading.Thread(target=apps.file_open, args=(model,))
        qqq.start()

    def start_button(self):
        qqq = threading.Thread(target=apps.go_run, args=(model,))
        qqq.start()

    # def file_button(self):
    #     qqq = threading.Thread(target=crawling.file_open, args=(model,))
    #     qqq.start()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        model = MyWindow()
        model.show()
        app.exec_()
        sys.exit(app.exec_())
    except:
        input("Press any key to exit the program....")
