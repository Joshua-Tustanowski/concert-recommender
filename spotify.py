"""
    App idea: Take in a list of artist names, and sort them by how much they match your saved music trends.
        Add on, from the favoured artists create a playlist of their best songs.
    Start a local server: python3 -m http.server --cgi 8080
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import os

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SECRET_ID = os.environ['SPOTIPY_CLIENT_SECRET']
REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']

scope = 'user-top-read'

logger = logging.getLogger('artist recommendations')
logging.basicConfig(level='INFO')


def print_artists_top_tracks(url):
    top_tracks = sp.artist_top_tracks(url)
    for track in top_tracks['tracks']:
        print(f"Name: {track['name']}")


def get_user_top_tracks():
    results = sp.current_user_top_tracks()
    for idx, item in enumerate(results['items']):
        track_name = item['name']
        artist = item['artists'][0]['name']
        print(f'{artist}: {track_name}')


def main(names):
    for name in names:
        artist = get_artist(name)
        if artist:
            show_recommendations_for_artist(artist)
        else:
            logger.error(f'Cannot find that artist: {artist}')


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    results = sp.recommendations(seed_artists=[artist['id']])
    for track in results['tracks']:
        logger.info('Recommendation: %s - %s', track['name'],
                    track['artists'][0]['name'])


if __name__ == "__main__":
    auth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=SECRET_ID,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
    auth_code = 'AQC-zU5sO600c0xyv_48QnfzsyknKf85GcMIFbecnQFv246flUK_q9e-oJhoLf24aRVxVh6rRq1nW5N7RsMBKvVmVkUM4PTJeK28dEP2O7PbyqSfQ0j2oxaWHOIoQpJYdFgUAurf78CR1heK2Nrri3_DISzjKSVYadcGH0_DrwWXAGrSvjugAuDYR5-RpYo_CuU'
    auth_token = auth.get_access_token(auth_code)
    sp = spotipy.Spotify(auth=auth_token['access_token'])
    artists = ['Arianna Grande', 'Dua Lipa', 'Harry Styles']
    # could sort by the users top 100 artists, find the recommendations for those artists and then see if the new
    # artists pop into these, have a counter for their occurrence and then sort by that list.
    main(artists)
