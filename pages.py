
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtCore import QObject,QThread,Signal
from windowUi import Ui_MainWidget
from dotenv import load_dotenv
from pprint import pprint
from testes import criaCsv
from utils import convertImgTo64,selectTrack,getLastFMSongsList,FEAT_REGEX
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import math
import os
import time

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

def convertSongsToSpotifyIds(songList,accessToken):
    songList = songList
    newSongList = []
    totalSongs = len(songList)
    songByFar = 0

    for i in songList:
        newName = FEAT_REGEX.sub('',i['name'])
        params = {
            "q": f"artist:{i['artist']} track:{newName}",
            "type": "track",
            "limit": 5
        }
        headers = {"Authorization": f"Bearer {accessToken}"}
        foundSong = requests.get(f'https://api.spotify.com/v1/search',
                                headers=headers,
                                params=params)


        # if not foundSong.json()['tracks']['items']:
        #     newName = FEAT_REGEX.sub('',i['name'])
        #     params['q'] = f"artist:{i['artist']} track:{newName}"

        #     foundSong = requests.get(f'https://api.spotify.com/v1/search',
        #                         headers=headers,
        #                         params=params)
            
        songByFar += 1
        perc = round((songByFar/totalSongs)*100,2)

        
        # print(f'{perc}% - Adicionando {i['artist']} - {i['name']}')
        # for y in foundSong.json()['tracks']['items']:
        #     print(f'Encontrado {y['name']} - {y['artists'][0]['name']}- {y['album']['name']} ')
        #     if not y:
        #         print(f'não encontrado a musica {i['artist']} - {i['name']}')
        # print('\n')

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

        songId = selectTrack(foundSongList,i)

        if songId: newSongList.append(songId)
        # newSongList.append(foundSongList)
        

    # exit()# finalList,self._missingSong = selectTrack(newSongList)
    return newSongList

class MainPage(Ui_MainWidget, QStackedWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self._userId = ''
        self._spotifyToken = ''
        self._missingSong = []
        self._percent = 0

        self.progressBar.setVisible(False)
        self.progressLabel.setVisible(False)
        self.loginButton.clicked.connect(self.loginOnSpotify)
        self.userButton.clicked.connect(self.createPlaylist)

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
        userImg = userData.json()['user']['image'][2]['#text']
        print(userImg)
        img = convertImgTo64(userImg)
        image_headers = {
                        "Authorization": f"Bearer {self._spotifyToken}",
                        "Content-Type": "image/png"
                        }
        

        songs = getLastFMSongsList(url)
        idList = convertSongsToSpotifyIds(songs,self._spotifyToken)
        playlistUrl = f'https://api.spotify.com/v1/users/{self._userId}/playlists'

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
        self.addSongsToPlaylist(idList,request['id'])

        print('Playlist criada com sucesso')
        print(imgRequest.status_code)


    def addSongsToPlaylist(self,songIdList,playlistId):
        url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'
        headers = {
            "Authorization": f"Bearer {self._spotifyToken}",
            "Content-Type": "application/json"}

        params = {'uris': []}
        songCounter = 0
        for index,i in enumerate(songIdList):
            songCounter += 1
            params['uris'].append(f'spotify:track:{i}')

            if songCounter == 100 or index == len(songIdList)-1:
                response = requests.post(url,headers=headers,json=params)
                print(response.status_code)
                params = {'uris': []}
                songCounter = 0



        
if __name__ == '__main__':...
