import requests
from config import SpotifyConfig
from dto import TrackFeature, RequestUrl, ArtistData, AlbumData, GetRequestResponse


class ApiCall:

    def __init__(self, api_config: SpotifyConfig):
        self.api_config = api_config
        self.keywords = {
            "type": 'track',
            "limit": 50
        }

    def search_request(self, keywords: dict, year: str, offset: int, dataset: list, song_dataset: list,
                           album_dataset: list, artist_dataset: list) -> list[dict] | requests.Response:
        offset = str(offset)
        api_call_limit = str(keywords["limit"])
        url = RequestUrl.GET_TRACK + year + '&type=' + keywords["type"] \
              + '&offset=' + offset + '&limit=' + api_call_limit
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.api_config.access_token})
        if request:
            request_json = request.json()
        else:
            return request
        track_search = request_json["tracks"]["items"]
        try:
            for track in track_search:
                get_request = GetRequestResponse()

                if track["id"] not in song_dataset:
                    song_dataset.append(track["id"])
                # else:
                #     song_dataset.append(track["id"])

                if track["artists"][0]["id"] not in artist_dataset:
                    artist_dataset.append(track["artists"][0]["id"])
                # else:
                #     artist_dataset.append(track["artists"][0]["id"])

                if track["album"]["id"] not in album_dataset:
                    album_dataset.append(track["album"]["id"])
                # else:
                #     album_dataset.append(track["album"]["id"])


                get_request["track_popularity"] = track["popularity"]
                get_request["song_id"] = track["id"]
                get_request["artist_id"] = track["artists"][0]["id"]
                get_request["album_id"] = track["album"]["id"]
                get_request["song_name"] = track["name"]
                get_request["artist_name"] = track["artists"][0]["name"]
                get_request["album_name"] = track["album"]["name"]

                dataset.append(get_request.request_response)
                del get_request
        except:
            ValueError
        return dataset

    def get_tracks_data(self, tracks_id: list, dataset: list) -> list[dict] | requests.Response:
        track_ids = ','.join(tracks_id)
        url = RequestUrl.GET_AUDIO_FEATURES + track_ids
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.api_config.access_token})
        request_json = request.json()
        if request:
            request_json = request.json()
        else:
            return request
        track_data = request_json["audio_features"]
        try:
            for track in track_data:
                track_feature = TrackFeature()
                for key in track_feature.request_response.keys():
                    track_feature[key] = track[key]

                dataset.append(track_feature.request_response)
                del track_feature
        except:
            ValueError

        return dataset

    def get_artist_data(self, artists_id: list, dataset: list) -> list[dict] | requests.Response:
        artist_ids = ','.join(artists_id)
        url = RequestUrl.GET_ARTISTS + artist_ids
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.api_config.access_token})
        request_json = request.json()
        if request:
            request_json = request.json()
        else:
            return request
        artist_data = request_json["artists"]
        try:
            for artist in artist_data:
                artist_feature = ArtistData()
                for key in artist_feature.request_response.keys():
                    artist_feature[key] = artist[key]

                dataset.append(artist_feature.request_response)
                del artist_feature
        except:
            ValueError

        return dataset

    def get_album_data(self, albums_id: list, dataset) -> list[dict] | requests.Response:
        album_ids = ','.join(albums_id)
        url = RequestUrl.GET_ALBUMS + album_ids
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.api_config.access_token})
        if request:
            request_json = request.json()
        else:
            return request
        album_data = request_json["albums"]
        try:
            for album in album_data:
                album_feature = AlbumData()
                for key in album_feature.request_response.keys():
                    album_feature[key] = album[key]

                dataset.append(album_feature.request_response)
                del album_feature
        except:
            ValueError

        return dataset
