import time

import pandas as pd
import requests
from config import SpotifyConfig
from dto import TrackFeature, RequestUrl, ArtistData
import spotipy


class ApiCall:
    auth_token = SpotifyConfig().access_token

    def __init__(self, api_config: SpotifyConfig):
        self.api_config = api_config


    def api_search_request(self, keywords: str, dataset ) -> list:

        return []

    def api_get_tracks_data(self, tracks_id: str, dataset: list) -> list:
        track_ids = ','.join(tracks_id)
        url = RequestUrl.GET_AUDIO_FEATURES + track_ids
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.auth_token})
        request_json = request.json()
        track_data = request_json["audio_features"]

        for track in track_data:
            track_feature = TrackFeature()
            for key in track_feature.request_response.items():
                track_feature[key] = track[key]

            dataset.append(track_feature)
            del track_feature

        return dataset

    def api_get_artist_data(self, artists_id: str, dataset: list) -> list:
        artist_ids = ','.join(artists_id)
        url = RequestUrl.GET_ARTISTS + artist_ids
        request = requests.get(url, headers={"Accept": "application/json", "Authorization": self.auth_token})
        request_json = request.json()
        artist_data = request_json["artist"]

        for artist in artist_data:
            artist_feature = ArtistData()
            for key in artist_feature.request_response.keys():
                artist_feature[key] = artist[key]

            dataset.append(artist_feature)
            del artist_feature


        return dataset

    def api_get_album_data(self, album_id: str, dataset) -> list:

        return []
