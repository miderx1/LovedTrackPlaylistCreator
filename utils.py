import requests
import math
import base64
import re
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

LASTFM_APY_KEY = os.getenv('LASTFM_API_KEY','')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID','')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET','')
REDIRECT_URI = 'http://127.0.0.1:8080/callback'

MOVIE_INDICATOR_REGEX = re.compile(r'\s[\(\[\-]\s?[fF]rom[^\-)]*[\]\)]?$'
                    ,flags=re.I)
FEAT_REGEX = re.compile(r'\s[\(\[\-]\s?((feat[uring]?\.?)|with)[^\-)]*[\]\)]?'
                    ,flags=re.I)

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
    try:
        foundSong = requests.get(f'https://api.spotify.com/v1/search',
                                headers=headers,
                                params=params)
    except requests.exceptions.RequestException:
        return 1



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

def splitlist(list,amount):
    count = 0
    lista = []
    itensPerList = len(list) // amount

    for i in range(len(list)):
        if count > itensPerList-1:
            yield lista.copy()
            count = 0
            lista.clear() 
        lista.append(list[i])
        count += 1
    yield lista.copy()

def getLastFMSongsList(url):
    initialResponse = requests.get(url)

    if initialResponse.status_code != 200:
        return None
    
    totalSongs = initialResponse.json()['lovedtracks']['@attr']['total']                    
    pages = math.ceil(int(totalSongs)/1000)
    songDicts = []
    counter = 0
    for i in range(pages):
        params = {'limit' : '1000','page': i+1}
        finalResponse = requests.get(url,params=params)

        if finalResponse.status_code != 200:
            print(finalResponse)
            return None
        
        songDictsList = finalResponse.json()['lovedtracks']['track']
        # print(songDictsList)
        for song in songDictsList:
            counter += 1 
            newName = MOVIE_INDICATOR_REGEX.sub('',song['name'])
            newSongDict = dict(
                name = newName,
                artist = song['artist']['name']
            )
            songDicts.append((counter,newSongDict))
    
    return(songDicts)


def selectTrack(foundList,song):
    idList = []
    newTrackName = FEAT_REGEX.sub('',song['name']).lower()
    selectedSong = {}

    if not foundList:
        print(f"não encontrada a Musica {song['name']} - {song['artist']}")
        return None
    
    for i in foundList:
        # pprint.pprint(i)
        newFoundTrackName = FEAT_REGEX.sub('',i['name']).lower()

        if i['albumType'] == 'album' and i['artist'] == song['artist']\
        and newFoundTrackName == newTrackName and i['albumArtist'] == song['artist']:
            selectedSong = i
            break
        
        elif i['albumType'] == 'album' and i['artist'] == song['artist']\
        and newFoundTrackName == newTrackName:
            selectedSong = i
            continue

        elif newTrackName == newFoundTrackName and i['albumType'] == 'album':
            selectedSong = i
        

    if not selectedSong:
        selectedSong = foundList[0]

    return selectedSong['id']

def convertImgTo64(image_url):

    try:
        # Baixa a imagem
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Verifica erros HTTP

        # Converte a imagem para Base64
        image_bytes = response.content
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        
        return base64_data

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

def searchExistent(array,item):
    for i in array:
        if item == i[1]:
            return True
    return False


if __name__ == '__main__':
    lista = ['25882','65848','582568','58995','5855','25882']

    print(list(set(lista)))