
from utils import (convertImgTo64,
                   getLastFMSongsList,
                   searchExistent,
                   splitlist,
                   convertSongsToSpotifyIds,
                   getSpotifyToken, 
                   LASTFM_APY_KEY)
from PySide6.QtCore import QObject,QThread,Signal,Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QStackedWidget
from windowUi import Ui_MainWidget
import requests
import time

class Worker(QObject):
    started = Signal()
    progressed = Signal(tuple,tuple)
    finished = Signal()

    def __init__(self,token):
        super().__init__()
        self._token = token
        self._songs = []

    def setSongs(self,songs):
        self._songs = songs

    @Slot()
    def execute(self):   
        self.started.emit()
        
        for song in self._songs:
            print(song)
            time.sleep(1)
            songId = (song[0],convertSongsToSpotifyIds(song[1], self._token))
            self.progressed.emit(song, songId)

        self.finished.emit()

class MainPage(Ui_MainWidget, QStackedWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self._userId = ''
        self._spotifyToken = ''
        self._missingSong = []
        self._percent = 0
        self._songIdList = []
        self._totalSong = 0
        self._threadsFinished = 0
        self._userImg = None

        self.setWindowTitle("Playlist Creator")
        self.loginButton.setProperty('cssClass','spotifyBtn')
        self.userButton.setProperty('cssClass','spotifyBtn')
        self.mainPageTitle.setProperty('cssClass','title')
        self.userInfo.setProperty('cssClass','warning')

        self.progressBar.setVisible(False)
        self.progressLabel.setVisible(False)
        self.progressLog.setVisible(False)
        self.loginButton.clicked.connect(self.loginOnSpotify)
        self.userButton.clicked.connect(self.createPlaylist)

    def hardwork(self,songs):
        worker = Worker(self._spotifyToken)
        thread = QThread()
        
        worker.setSongs(songs)
        worker.moveToThread(thread)

        thread.started.connect(worker.execute)
        worker.finished.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)

        worker.started.connect(self.workerStarted)
        worker.progressed.connect(self.workerProgressed)
        worker.finished.connect(self.workerFinished)

        if not hasattr(self, "_activeThreads"):
            self._activeThreads = []

        self._activeThreads.append((thread, worker))
        thread.start()

    def workerStarted(self):
        self.userButton.setDisabled(True)
        self.userInput.setDisabled(True)

    def workerProgressed(self,song,songId):
        if songId == 1:
            self.userInfo.setText('Erro de conexão')
            self.progressLog.clear()
            self.progressLog.insertPlainText(f'Erro de conexão. Tente Novamente')
            return

        self._percent = round((len(self._songIdList) / self._totalSong)*100,2)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(self._percent)


        songStr = f'{song[1]['artist']} - {song[1]['name']}'


        if songId[1] and not searchExistent(self._songIdList,songId[1]):
            self._songIdList.append(songId)
            self.progressLog.insertPlainText(f'{songStr}\n')

        elif searchExistent(self._songIdList,songId[1]):
            self.progressLog.insertPlainText(f'{songStr} já existe na lista\n')

        self.progressLog.moveCursor(QTextCursor.End)

    def workerFinished(self):
        self._threadsFinished += 1

        if self._threadsFinished == self._totalThreads:
            self.continueExec()

    def continueExec(self):
        user = self.userInput.text()

        print(self._userImg)
        img = convertImgTo64(self._userImg)
        image_headers = {
                        "Authorization": f"Bearer {self._spotifyToken}",
                        "Content-Type": "image/png"
        }
        


        playlistUrl = f'https://api.spotify.com/v1/me/playlists'

        headers = {
                    "Authorization": f"Bearer {self._spotifyToken}",
                    "Content-Type": "application/json"
        }
        data = {
                "name": f"Musicas favoritas de {user}",
                "description": f"Musicas marcadas como favoritas no perfil de {user}, no Last.FM",
                "public": False
        } 

        request = (requests.post(playlistUrl, headers=headers, json=data)).json()

        imgUrl = f"https://api.spotify.com/v1/playlists/{request['id']}/images"

        imgRequest = requests.put(imgUrl, headers=image_headers, data=img)
        self.addSongsToPlaylist(request['id'])


    def loginOnSpotify(self):
        self._spotifyToken = getSpotifyToken()
        headers = {"Authorization": f"Bearer {self._spotifyToken}"}
        user = requests.get('https://api.spotify.com/v1/me', headers=headers)
        self._userId = user.json()['id']
        self.setCurrentWidget(self.mainPage)
        self.userInput.setFocus()
    
    def createPlaylist(self):
        self.progressLog.clear()
        self.userInfo.clear()
        user = self.userInput.text()
        apiKey = LASTFM_APY_KEY

        url = f'https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={user}&api_key={apiKey}&format=json'
        userUrl = f'https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={user}&api_key={apiKey}&format=json'

        userData = requests.get(userUrl)
        try:
            self._userImg = userData.json()['user']['image'][2]['#text']
            self.progressLog.setVisible(True)
            songs = getLastFMSongsList(url)
            
            splitedSongs = [i for i in splitlist(songs,10)]

            self._totalThreads = len(splitedSongs)

            self._totalSong = len(songs)
            
            for part in splitedSongs:
                self.hardwork(part)
            
        except KeyError:
            self.userInfo.setText('O usuário informado não existe')
            
    def addSongsToPlaylist(self,playlistId):
        self.progressBar.setValue(99)
        self.progressLabel.setText('99')

        sortedList = sorted(self._songIdList, key=lambda song: song[0])

        url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'
        headers = {
            "Authorization": f"Bearer {self._spotifyToken}",
            "Content-Type": "application/json"}

        params = {'uris': []}
        songCounter = 0

        for index,i in enumerate(sortedList):
            songCounter += 1
            params['uris'].append(f'spotify:track:{i[1]}')

            if songCounter == 100 or index == len(sortedList)-1:
                requests.post(url,headers=headers,json=params)
                params = {'uris': []}
                songCounter = 0

        self._missingSong = []
        self._percent = 0
        self._songIdList = []
        self._totalSong = 0
        self._threadsFinished = 0
        self.userInput.setDisabled(False)
        self.userButton.setDisabled(False)
        self.progressBar.setValue(100)
        self.progressLabel.setText('100')
        self.progressLog.insertPlainText(f'Playlist criada com sucesso')

if __name__ == '__main__':...
