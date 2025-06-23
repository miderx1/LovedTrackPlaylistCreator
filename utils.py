import requests
import math
import base64
import re
import pprint

MOVIE_INDICATOR_REGEX = re.compile(r'\s[\(\[\-]\s?[fF]rom[^\-)]*[\]\)]?$'
                    ,flags=re.I)
FEAT_REGEX = re.compile(r'\s[\(\[\-]\s?((feat[uring]?\.?)|with)[^\-)]*[\]\)]?'
                    ,flags=re.I)

def getLastFMSongsList(url):
    initialResponse = requests.get(url)

    if initialResponse.status_code != 200:
        return None
    
    totalSongs = initialResponse.json()['lovedtracks']['@attr']['total']                    
    pages = math.ceil(int(totalSongs)/1000)
    songDicts = []

    for i in range(pages):
        params = {'limit' : '1000','page': i+1}
        finalResponse = requests.get(url,params=params)

        if finalResponse.status_code != 200:
            print(finalResponse)
            return None
        
        songDictsList = finalResponse.json()['lovedtracks']['track']
        # print(songDictsList)
        for song in songDictsList:
            newName = MOVIE_INDICATOR_REGEX.sub('',song['name'])
            newSongDict = dict(
                name = newName,
                artist = song['artist']['name']
            )
            songDicts.append(newSongDict)
    
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


if __name__ == '__main__':
    img = 'https://lastfm.freetls.fastly.net/i/u/avatar170s/a37047f0a570a2ba31c94d6dc9e809a9.png'
    print(convertImgTo64(img))