# default imports
import sys
from interfaces import login
from PyQt5.QtWidgets import QApplication


# master function that triggers the Ui
def main():
    if __name__ == "__main__":
        application = QApplication(sys.argv)
        clearout_phone_window = login.LoginWindow()
        clearout_phone_window.show()
        application.exec_()


main()