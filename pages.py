
from utils import convertImgTo64,selectTrack,getLastFMSongsList,FEAT_REGEX
from PySide6.QtCore import QObject,QThread,Signal,Slot
from PySide6.QtWidgets import QStackedWidget
from spotipy.oauth2 import SpotifyOAuth
from windowUi import Ui_MainWidget
from dotenv import load_dotenv
import requests
import os

load_dotenv()

LASTFM_APY_KEY = os.getenv('LASTFM_API_KEY','')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID','')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET','')
REDIRECT_URI = 'http://127.0.0.1:8080/callback'

def getSpotifyToken():
    scope = 'playlist-modify-private user-read-private ugc-image-upload'
    
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    )

    # Tenta obter o token do cache (se existir)
    token_info = auth_manager.get_cached_token()

    # Se não houver token no cache ou estiver expirado, inicia o fluxo de autenticação
    if not token_info or auth_manager.is_token_expired(token_info):
        print("Token inválido ou expirado. Gerando novo...")
        auth_url = auth_manager.get_authorize_url()
        print("Acesse esta URL e autorize:", auth_url)
        
        # Aguarda o usuário autorizar e retorna o novo token
        token_info = auth_manager.get_access_token(as_dict=True)
    
    # Retorna o token de acesso (string)
    return token_info['access_token']

def convertSongsToSpotifyIds(song,accessToken):
    song = song
    newName = FEAT_REGEX.sub('',song['name'])

    params = {
        "q": f"artist:{song['artist']} track:{newName}",
        "type": "track",
        "limit": 5
    }

    headers = {"Authorization": f"Bearer {accessToken}"}
    foundSong = requests.get(f'https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)


    foundSongList = []
    for j in foundSong.json()['tracks']['items']:
        foundSongDict = dict(
            name = j['name'],
            artist = j['artists'][0]['name'],
            album = j['album']['name'],
            albumType = j['album']['album_type'],
            albumArtist = j['album']['artists'][0]['name'],
            id = j['id'],
            explict = j['explicit']
        )
        foundSongList.append(foundSongDict)

    songId = selectTrack(foundSongList,song)

    return songId

def splitList(list):
    list1 = []
    list2 = []

    for index,item in enumerate(list):
        if index <= len(list)/2:
            list1.append(item)
        else:
            list2.append(item)

    return [list1,list2],len(list)

class Worker(QObject):
    started = Signal()
    progressed = Signal(dict,str)
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
            songId = convertSongsToSpotifyIds(song, self._token)
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
        self._totalThreads = 2
        self._userImg = None

        self.progressBar.setVisible(False)
        self.progressLabel.setVisible(False)
        self.loginButton.clicked.connect(self.loginOnSpotify)
        self.userButton.clicked.connect(self.createPlaylist)

    def hardwork(self,songs):
        self._worker = Worker(self._spotifyToken)
        self._thread = QThread()
        
        worker = self._worker
        thread = self._thread
        worker.setSongs(songs)

        worker.moveToThread(thread)

        thread.started.connect(worker.execute)

        worker.finished.connect(thread.quit)

        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)

        worker.started.connect(self.workerStarted)
        worker.progressed.connect(self.workerProgressed)
        worker.finished.connect(self.workerFinished)

        thread.start()
    def hardwork2(self,songs):
        self._worker2 = Worker(self._spotifyToken)
        self._thread2 = QThread()
        
        worker2 = self._worker2
        thread2 = self._thread2

        worker2.setSongs(songs)
        
        worker2.moveToThread(thread2)

        thread2.started.connect(worker2.execute)

        worker2.finished.connect(thread2.quit)

        thread2.finished.connect(thread2.deleteLater)
        worker2.finished.connect(worker2.deleteLater)

        worker2.started.connect(self.workerStarted)
        worker2.progressed.connect(self.workerProgressed)
        worker2.finished.connect(self.workerFinished)

        thread2.start()


    def workerStarted(self):
        print('Processo Iniciado')
        self.userButton.setDisabled(True)
        self.userInput.setDisabled(True)

    def workerProgressed(self,song,songId):
        if songId:
            self._songIdList.append(songId)
        self._percent = round((len(self._songIdList) / self._totalSong)*100,2)
        print(f'{self._percent}% - {song}')

    def workerFinished(self):

        self._threadsFinished += 1
        print(f'Thread finalizada ({self._threadsFinished}/{self._totalThreads})')

        if self._threadsFinished == self._totalThreads:
            print('100% - Todas as threads finalizaram')
            print(self._songIdList)
            self.continueExec()

    def continueExec(self):
        user = self.userInput.text()
        print("OOOOOOOOOOOOOOIIIIIIIIIIIIIIIIIIIIIIII")

        print(self._userImg)
        img = convertImgTo64(self._userImg)
        image_headers = {
                        "Authorization": f"Bearer {self._spotifyToken}",
                        "Content-Type": "image/png"
                        }
        


        playlistUrl = f'https://api.spotify.com/v1/users/{self._userId}/playlists'

        headers = {
                    "Authorization": f"Bearer {self._spotifyToken}",
                    "Content-Type": "application/json"
        }
        data = {
                "name": f"Musicas favoritas de {user}",
                "description": f"Musicas marcadas como favoritas no perfil de {user}, no Last.FM",
                "public": 'false'
        } 

        request = (requests.post(playlistUrl, headers=headers, json=data)).json()

        imgUrl = f"https://api.spotify.com/v1/playlists/{request['id']}/images"

        imgRequest = requests.put(imgUrl, headers=image_headers, data=img)
        self.addSongsToPlaylist(request['id'])

        print('Playlist criada com sucesso')
        print(imgRequest.status_code)


    def loginOnSpotify(self):
        self._spotifyToken = getSpotifyToken()
        headers = {"Authorization": f"Bearer {self._spotifyToken}"}
        user = requests.get('https://api.spotify.com/v1/me', headers=headers)
        self._userId = user.json()['id']
        self.setCurrentWidget(self.mainPage)
        print(user.json())
        print(self._spotifyToken)
    
    def createPlaylist(self):
        user = self.userInput.text()
        apiKey = LASTFM_APY_KEY

        url = f'https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={user}&api_key={apiKey}&format=json'
        userUrl = f'https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={user}&api_key={apiKey}&format=json'

        userData = requests.get(userUrl)
        self._userImg = userData.json()['user']['image'][2]['#text']
        songs = getLastFMSongsList(url)
        splitedSongs,self._totalSong = splitList(songs)
        
        self.hardwork(splitedSongs[0])
        self.hardwork2(splitedSongs[1])
        

    def addSongsToPlaylist(self,playlistId):
        print(self._songIdList)

        url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'
        headers = {
            "Authorization": f"Bearer {self._spotifyToken}",
            "Content-Type": "application/json"}

        params = {'uris': []}
        songCounter = 0

        for index,i in enumerate(self._songIdList):
            songCounter += 1
            params['uris'].append(f'spotify:track:{i}')

            if songCounter == 100 or index == len(self._songIdList)-1:
                response = requests.post(url,headers=headers,json=params)
                print(response.status_code)
                params = {'uris': []}
                print(params)
                songCounter = 0

        self.userInput.setDisabled(False)
        self.userButton.setDisabled(False)

        
if __name__ == '__main__':...
