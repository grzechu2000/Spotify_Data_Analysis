import time

import pandas as pd
import requests
from config import SpotifyConfig
import spotipy

config = SpotifyConfig()

def main():
    queries = ['1995']
    num_tracks_per_query = 10000



    for query in queries:

        ltrack = []
        song_ids = []
        artist_ids = []
        album_ids = []

        audioF = []
        artist_data = []
        album_data = []

        col1 = ['popularity',
                'song_id', 'artist_id', 'album_id',
                'song_name', 'artist_name', 'album_name',
                'explicit', 'disc_number', 'track_number']

        col2 = ['song_id', 'uri',
                'tempo', 'type',
                'key', 'loudness',
                'mode', 'speechiness',
                'liveness', 'valence',
                'danceability', 'energy',
                'track_href', 'analysis_url',
                'duration_ms', 'time_signature',
                'acousticness', 'instrumentalness']

        col3 = ['artist_id', 'artist_genres', 'artist_popularity']

        col4 = ['album_id', 'album_genres', 'album_popularity', 'album_release_date']

        n = 0
        idx = 0

        while idx < num_tracks_per_query:
            API_search_request(query, 'track', 50, idx, ltrack, song_ids, artist_ids, album_ids, config.access_token)
            n += 1
            print(('\n>> this is No ' + str(n) + ' search End '))
            idx += 50
            # Limit API requests to at most 3ish calls / second
            time.sleep(0.3)

        print(len(song_ids))
        ## spotify API "search" option vs here track/audiofeature query
        for idx in range(0, len(song_ids), 50):
            API_get_audio_feature(song_ids[idx: idx + 50], audioF, config.access_token)
            time.sleep(0.3)

        for idx in range(0, len(artist_ids), 50):
            API_get_artists(artist_ids[idx: idx + 50], artist_data, config.access_token)
            time.sleep(0.3)

        for idx in range(0, len(album_ids), 20):
            API_get_albums(album_ids[idx: idx + 20], album_data, config.access_token)
            time.sleep(0.3)

        df1 = pd.DataFrame(ltrack, columns=col1)

        df2 = pd.DataFrame(audioF, columns=col2)

        df3 = pd.DataFrame(artist_data, columns=col3)

        df4 = pd.DataFrame(album_data, columns=col4)

        df = df1.merge(df2, on='song_id', how='outer').merge(df3, on='artist_id', how='outer').merge(
            df4, on='album_id', how='outer')

        filename = query + '.csv'

        df.to_csv(filename, sep='\t')

        print('finish')
        print(query)


def API_search_request(keywords, search_type, results_limit, results_offset, ltrack, song_ids, artist_ids, album_ids, token):
    off = str(results_offset)
    lim = str(results_limit)

    url = 'https://api.spotify.com/v1/search?q=year:' + keywords + '&type=' + search_type + '&offset=' + off + '&limit=' + lim

    r = requests.get(url, headers={"Accept": "application/json", "Authorization": token})


    if r:
        j = r.json()
    else:
        return r

    litem = j['tracks']['items']
    # print(len(ll))
    try:
        for l in litem:

            if l['id'] not in song_ids:
                song_ids.append(l['id'])

            if l['artists'][0]['id'] not in artist_ids:
                artist_ids.append(l['artists'][0]['id'])

            if l['album']['id'] not in album_ids:
                album_ids.append(l['album']['id'])

            k = [l['popularity'],

                 l['id'],
                 l['artists'][0]['id'],
                 l['album']['id'],

                 l['name'],
                 l['artists'][0]['name'],
                 l['album']['name'],

                 l['explicit'],
                 l['disc_number'],
                 l['track_number']]

            ltrack.append(k)
    except:
        ValueError


def API_get_audio_feature(songids, audioF, token):
    track_ids = ','.join(songids)

    url = 'https://api.spotify.com/v1/audio-features?ids=' + track_ids

    r = requests.get(url, headers={"Accept": "application/json", "Authorization": token})

    if r:
        j = r.json()
    else:
        return r

    # print(j)
    ll = j['audio_features']

    try:

        for l in ll:
            k = [l['id'], l['uri'],
                 l['tempo'], l['type'],
                 l['key'], l['loudness'],
                 l['mode'], l['speechiness'],
                 l['liveness'], l['valence'],
                 l['danceability'], l['energy'],
                 l['track_href'], l['analysis_url'],
                 l['duration_ms'], l['time_signature'],
                 l['acousticness'], l['instrumentalness']]

            audioF.append(k)

    except:
        ValueError


def API_get_artists(artist_ids, artist_data, token):
    art_ids = ','.join(artist_ids)

    url = 'https://api.spotify.com/v1/artists?ids=' + art_ids

    r = requests.get(url, headers={"Accept": "application/json", "Authorization": token})

    if r:
        j = r.json()
    else:
        return r

    ll = j['artists']

    try:
        for l in ll:
            k = [l['id'],
                 l['genres'],
                 l['popularity']]

            artist_data.append(k)

    except:
        ValueError


def API_get_albums(album_ids, album_data, token):
    alb_ids = ','.join(album_ids)

    url = 'https://api.spotify.com/v1/albums?ids=' + alb_ids

    r = requests.get(url, headers={"Accept": "application/json", "Authorization": token})

    if r:
        j = r.json()
    else:
        return r

    ll = j['albums']

    try:
        for l in ll:
            k = [l['id'],
                 l['genres'],
                 l['popularity'],
                 l['release_date']]

            album_data.append(k)

    except:
        ValueError


if __name__ == '__main__':
    main()
