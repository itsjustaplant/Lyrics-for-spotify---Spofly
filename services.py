import base64
import json
import requests
from flask import redirect, request, session

CLIENT_ID = "94bc89eaaa30437aba608352e9de4565"
CLIENT_SECRET = "77765644dc0140e99da1113454e42c29"
SPOTIFY_URL = "https://accounts.spotify.com"
SPOTIFY_API_URL = "https://api.spotify.com"
COLORFLY_BASE_URL = "http://colorflyv1.herokuapp.com/v1/"
REDIRECT_URI = "https://spoflyv1.herokuapp.com/callback"
LOCAL_URI = "http://localhost:5000/callback"
SCOPE = "user-read-currently-playing"


# Login with spotify
def login():
    return SPOTIFY_URL + \
           "/authorize?client_id=" + CLIENT_ID + \
           "&response_type=code&redirect_uri=" + LOCAL_URI +  \
           "&scope=" + SCOPE


# Get token from callback
def callback():
    session['auth_token'] = request.args['code']
    session['code_payload'] = {
        'grant_type': 'authorization_code',
        'code': str(session['auth_token']),
        'redirect_uri': LOCAL_URI
    }
    base = "{}:{}"
    format_client = base.format(CLIENT_ID, CLIENT_SECRET)
    base64encoded = base64.urlsafe_b64encode(format_client.encode()).decode()
    session['headers'] = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_URL + "/api/token", data=session['code_payload'],
                                 headers=session['headers'])
    response_data = json.loads(post_request.text)
    session['access_token'] = response_data['access_token']
    session['authorization_header'] = {'Authorization': 'Bearer {}'.format(session['access_token'])}


# Get song from api.spotify and return song, artist, refresh_ms, local flag and artwork url
# TODO: deprecate the refresh_ms to refresh the page
def get_song():
    token = session.get("access_token")
    if token:
        headers = {
            "Authorization": "Bearer {}".format(session['access_token'])
        }
        current_song = requests.get(SPOTIFY_API_URL + "/v1/me/player/currently-playing", headers=headers)
        # Check if user is listening a song if not try again by redirecting to /lyrics
        if current_song.status_code == 204:
            return redirect("/lyrics")
        # Force page to get song :^
        while current_song.status_code != 200:
            current_song = requests.get(SPOTIFY_URL + "/v1/me/player/currently_playing", headers=headers)
        current_song_json = current_song.json()
        song = current_song_json['item']['name']
        artist = current_song_json['item']['artists'][0]['name']
        duration_ms = current_song_json['item']['duration_ms']
        progress_ms = current_song_json['progress_ms']
        refresh_ms = (duration_ms - progress_ms) / 1000 - 15
        # If refresh time is negative make it positive :^
        if refresh_ms < 0:
            refresh_ms *= -1
        is_local = current_song_json['item']['is_local']
        artwork_url = current_song_json['item']['album']['images'][0]['url']
        return song, artist, refresh_ms, is_local, artwork_url


# Get background color and suitable text color from colorfly API
def get_colors(flag, url):
    if flag == bool(0):
        response = requests.get(COLORFLY_BASE_URL + "color/" + url)
        response_json = response.json()
        return response_json['color_0'], response_json['color_1']


# Get lyrics from colorfly API
def get_lyrics(artist, song):
    if artist and song:
        data = {
            "artist": artist,
            "song": song
        }
        response = requests.post(url=COLORFLY_BASE_URL + "lyrics/", data=data)
        return response.json()['lyrics']
