class RequestUrl:
    GET_ALBUMS = 'https://api.spotify.com/v1/albums?ids='
    GET_ARTISTS = 'https://api.spotify.com/v1/artists?ids='
    GET_AUDIO_FEATURES = 'https://api.spotify.com/v1/audio-features?ids='
    GET_TRACK = 'https://api.spotify.com/v1/search?q=year:'


class GetRequestResponse:

    def __init__(self):
        self.request_response = {
            "track_popularity": int,
            "song_id": str,
            "artist_id": str,
            "album_id": str,
            "song_name": str,
            "artist_name": str,
            "album_name": str
        }

    def __getitem__(self, item):
        return self.request_response[item]

    def __setitem__(self, key, value):
        self.request_response[key] = value


class TrackFeature:
    def __init__(self):
        self.request_response = {
            "acousticness": float,
            "analysis_url": str,
            "danceability": float,
            "duration_ms": int,
            "energy": float,
            "id": str,
            "instrumentalness": float,
            "key": int,
            "liveness": float,
            "loudness": float,
            "mode": int,
            "speechiness": float,
            "tempo": float,
            "time_signature": int,
            "track_href": str,
            "type": str,
            "uri": str,
            "valence": float
        }

    def __getitem__(self, item):
        return self.request_response[item]

    def __setitem__(self, key, value):
        self.request_response[key] = value


class ArtistData:
    def __init__(self):
        self.request_response = {
            "id": str,
            "genres": list,
            "popularity": int
        }

    def __getitem__(self, item):
        return self.request_response[item]

    def __setitem__(self, key, value):
        self.request_response[key] = value


class AlbumData:
    def __init__(self):
        self.request_response = {
            "id": str,
            "genres": list,
            "popularity": int,
            "release_date": str
        }

    def __getitem__(self, item):
        return self.request_response[item]

    def __setitem__(self, key, value):
        self.request_response[key] = value
