
qss = f"""
    QWidget{{
        background: #121212;
    }}
    QLabel[cssClass="title"]{{
        color: #fff;
        font-weight: bold;
        font-size: 20px;
    }}
    QLabel[cssClass="warning"]{{
        color: #F00;

    }}
    QPushButton[cssClass="spotifyBtn"] {{
        color: #000;
        font-weight: bold;
        background: #1ED760;
        border-radius: 25px;
        font-size: 15px;
        width: 300px;
        height: 50px;
    }}

    QPushButton[cssClass="spotifyBtn"]:hover {{   
        font-size: 16px;
        background: #67eb96;
    }}

    QLabel{{
        color: #FFF;
        font-weight: bold;
    }}
    QLineEdit{{
        height: 40px;
        font-size: 20px;
        color: #FFF;
    }}
    QPlainTextEdit{{
        color: #FFF; 
    }}
    QProgressBar{{
        color: #FFF;
    }}
    QProgressBar {{
        border: 2px solid #555;
        border-radius: 5px;
        color: #FFF;
        text-align: center;
        background-color: #000;
    }}

    QProgressBar::chunk {{
        background-color: #1ED760;
        width: 2px;
    }}

"""

def setupTheme(app):
    app.setStyleSheet(app.styleSheet() + qss)