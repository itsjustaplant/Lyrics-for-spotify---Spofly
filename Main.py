from flask import Flask, render_template, redirect, request, session
import requests
import json
import base64
import lyricsgenius
import os

app = Flask(__name__)
app.secret_key=os.urandom(20)
CLIENT_ID = "e6cd36c6ea1c44b09245097b9e3367e1"
CLIENT_SECRET = "94c8b9efa0f34440b7c3225b75ff0b37"
GENIUS_URL = "http://www.genius.com/"
genius = lyricsgenius.Genius("YXICHA95DGXKPPPkXp-iSddKqjf93dOfxM30rG2s168h6t721l6WGcDt8KpGVO7G")

@app.route("/")
def login():
    return render_template(("login.html"))
@app.route("/login")
def log():
    return redirect(
        "https://accounts.spotify.com/authorize?client_id="+CLIENT_ID+"&response_type=code&redirect_uri=https://spoflyv1.herokuapp.com/callback&scope=user-read-private user-read-email user-read-currently-playing user-modify-playback-state")

@app.route("/callback")
def token():
    session['auth_token'] = request.args['code']
    session['code_payload'] = {
        'grant_type': 'authorization_code',
        'code': str(session['auth_token']),
        'redirect_uri': 'https://spoflyv1.herokuapp.com/callback'
    }
    base = "{}:{}"
    format_client = base.format(CLIENT_ID, CLIENT_SECRET)
    base64encoded = base64.urlsafe_b64encode(format_client.encode()).decode()
    session['headers'] = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post("https://accounts.spotify.com/api/token", data=session['code_payload'],
                             headers=session['headers'])
    response_data = json.loads(post_request.text)
    session['access_token'] = response_data['access_token']
    session['authorization_header'] = {'Authorization': 'Bearer {}'.format(session['access_token'])}
    return redirect("/lyrics")

@app.route("/lyrics")
def init():
    token = session.get("access_token")
    if token:
        headers = {
            "Authorization": "Bearer {}".format(session['access_token'])
        }
        spotify = requests.get("https://api.spotify.com/v1/me/player/currently_playing", headers=headers)
        while spotify.status_code != 200:
            spotify = spotify = requests.get("https://api.spotify.com/v1/me/player/currently_playing", headers=headers)
        current_song = spotify.json()
        song_title = current_song['item']['name']
        artist_name = current_song['item']['artists'][0]['name']
        if current_song['item']['is_local'] == bool(0):
            image_url = current_song['item']['album']['images'][0]['url']
        else:
            image_url = ""
        duration_ms = current_song['item']['duration_ms']
        progress_ms = current_song['progress_ms']
        refresh_ms = (duration_ms - progress_ms) / 1000 - 15

        if refresh_ms < 0:
            refresh_ms *= -1

        if song_title and artist_name:
            song = genius.search_song(title=song_title, artist=artist_name)

            if song != None:
                lyrics = song.lyrics

            else:
                lyrics = "lyrics not found"

        else:
            lyrics = "if you are playing a local file please edit metadata"

        return render_template("home.html", data=lyrics, artist_name=artist_name, song_title=song_title,
                               image=image_url, refresh_ms=refresh_ms)

    else:
        print("hey")
        return redirect("/login")

@app.route("/next")
def next():
    headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }
    requests.post("https://api.spotify.com/v1/me/player/next",headers=headers)
    return redirect("/lyrics")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
if __name__ == '__main__':
    app.run()

