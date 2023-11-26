import time

import pandas as pd
from api_calls import ApiCall
from config import SpotifyConfig


def main():
    config = SpotifyConfig()
    api = ApiCall(config)
    years = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
             '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
             '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'
             ]

    for year in years:
        dataset = []
        song_ids = []
        album_ids = []
        artist_ids = []
        song_features = []
        album_features = []
        artist_features = []

        lule = 1000
        idx = 0
        while idx < lule:
            dataset = api.search_request(api.keywords, year, idx, dataset, song_ids, album_ids, artist_ids)
            idx += 50
            time.sleep(0.3)

        print("Finished acquiring music data for ", year)

        for idx in range(0, len(song_ids), 50):
            song_features = api.get_tracks_data(song_ids[idx: idx + 50], song_features)
            time.sleep(0.3)

        for idx in range(0, len(album_ids), 20):
            album_features = api.get_album_data(album_ids[idx: idx + 20], album_features)
            time.sleep(0.3)

        for idx in range(0, len(artist_ids), 50):
            artist_features = api.get_artist_data(artist_ids[idx: idx + 50], artist_features)
            time.sleep(0.3)

        df_tracks = pd.DataFrame(dataset)
        df_features = pd.DataFrame(song_features)
        df_artists = pd.DataFrame(artist_features)
        df_albums = pd.DataFrame(album_features)

        df = df_tracks.merge(df_features, left_on='song_id', right_on='id').merge(
            df_artists, left_on='artist_id', right_on='id').merge(
            df_albums, left_on='album_id', right_on='id')
        df.to_csv(year + '.csv')

if __name__ == '__main__':
    main()
