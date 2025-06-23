import requests
from dotenv import load_dotenv
from pprint import pprint
import sys
from pages import MainPage
from PySide6.QtWidgets import QApplication

# load_dotenv()

# LASTFM_KEY  = os.getenv('LASTFM_API_KEY','')
# print(LASTFM_KEY)
# URL_REQUEST = f'https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=surrealan&api_key={LASTFM_KEY}&format=json'

# loved = requests.get(URL_REQUEST)

# pprint(loved.json())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    app.exec()