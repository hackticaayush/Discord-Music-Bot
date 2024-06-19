from ytmusicapi import YTMusic
from urllib.parse import quote, unquote

ytmusic = YTMusic()

def getResult(serch_value:str, isVideo: bool) -> []: # type: ignore
    if isVideo:
        search_filter = "videos"
    else: 
        search_filter = "songs"
    search_results = ytmusic.search(serch_value, filter= search_filter, ignore_spelling=False)
    result_list = []
    for i in range(min(len(search_results), 10)):
        name = search_results[i].get('title', '')
        artlistList = search_results[i].get('artists', '[]')
        thumbnail = search_results[i].get('thumbnails', '[]')[0].get('url')
        videoId = search_results[i].get('videoId' '')
        artistName = ""
        if len(artlistList) != 0 :
            for j in range(len(artlistList)):
                if not artistName == "":
                    if not j == len(artlistList)-1:
                        artistName = artistName + ", " + artlistList[j].get('name')
                    else: 
                        artistName = artistName + " & " + artlistList[j].get('name')
                else: 
                    artistName = artlistList[j].get('name')
        temp1 = quote(name)
        temp2 = quote(artistName)
        result_list.append('{"name": "' + temp1 + '", "artist": "' + temp2 + '", "thumbnail": "' + thumbnail + '", "videoId": "' + videoId + '"}')
    #print(result_list)
    return result_list



