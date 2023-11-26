from spotipy.oauth2 import SpotifyClientCredentials
from access_keys import Keys


class SpotifyConfig:

    @property
    def access_token(self):
        return SpotifyClientCredentials(Keys.CLIENT_ID, Keys.CLIENT_SECRET).get_access_token()['token_type'] + ' ' + \
            SpotifyClientCredentials(Keys.CLIENT_ID, Keys.CLIENT_SECRET).get_access_token()['access_token']
