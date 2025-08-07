from dotenv import load_dotenv
from pprint import pprint
import sys
from pages import MainPage
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    app.exec()