from dotenv import load_dotenv
from pprint import pprint
import sys
from pages import MainPage
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from styles import setupTheme
from pathlib import Path

ICON_PATH = Path(__file__).parent / 'src' / 'Icon.png'

if sys.platform == "win32":
    import ctypes
    myappid = 'mycompany.myapp.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    app.setWindowIcon(QIcon(str(ICON_PATH)))
    setupTheme(app)
    app.exec()