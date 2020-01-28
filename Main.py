from flask import Flask, render_template, redirect, request, session
import requests
import json
import base64
import lyricsgenius
import os
from colorthief import ColorThief
import urllib.request
import io
import ssl
app = Flask(__name__)
app.secret_key = os.urandom(20)
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
        "https://accounts.spotify.com/authorize?client_id=" + CLIENT_ID + "&response_type=code&redirect_uri=https://spoflyv1.herokuapp.com/callback&scope=user-read-private user-read-email user-read-currently-playing user-modify-playback-state")


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
        if spotify.status_code==204:
            return redirect("/favs")

        while spotify.status_code != 200:
            spotify = spotify = requests.get("https://api.spotify.com/v1/me/player/currently_playing", headers=headers)
        current_song = spotify.json()
        song_id = current_song['item']['id']
        song_title = current_song['item']['name']
        artist_name = current_song['item']['artists'][0]['name']
        duration_ms = current_song['item']['duration_ms']
        progress_ms = current_song['progress_ms']
        refresh_ms = (duration_ms - progress_ms) / 1000 - 15
        if refresh_ms < 0:
            refresh_ms *= -1

        if current_song['item']['is_local'] == bool(0):
            context = ssl._create_unverified_context()
            image_url = current_song['item']['album']['images'][0]['url']
            fd = urllib.request.urlopen(image_url,context=context)
            f = io.BytesIO(fd.read())
            color_thief = ColorThief(f)
            palette = color_thief.get_palette(color_count=6)

            def rgb2hex(r, g, b):
                return "#{:02x}{:02x}{:02x}".format(r, g, b)


            a = 1 - (0.299 * palette[0][0] + 0.587 * palette[0][1] + 0.114 * palette[0][2]) / 255
            print(a)
            if a<0.5:
                col_2="#000000"
            else:
                col_2="#FFFFFF"

            col_1 = rgb2hex(palette[0][0],palette[0][1],palette[0][2])
            col_3 = rgb2hex(palette[2][0], palette[2][1], palette[2][2])

            if song_title and artist_name:
                song = genius.search_song(title=song_title, artist=artist_name)

                if song!=None:
                    lyrics = song.lyrics

                else:
                    lyrics = "lyrics not found"

            else:
                lyrics = "if you are playing a local file please edit metadata"

            return render_template("home.html",bg_color=col_1,txt_color=col_2, data=lyrics, artist_name=artist_name, song_title=song_title,
                                   image=image_url, refresh_ms=refresh_ms, shadow=col_3)

        else:
            return render_template("404.html",data= "you have reached the end of the internet ",artist_name=artist_name,song_title=song_title,refresh_ms=refresh_ms)



    else:
        return redirect("/login")

@app.route("/next")
def next():
    headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }
    requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    return redirect("/lyrics")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/favs")
def favs():
    return render_template("favs.html")


@app.route("/trck1")
def rec1():
    headers = {"Authorization": "Bearer {}".format(session['access_token']), 'Accept': 'application/json',
               "Content-Type": "application/json"}

    body = {
        "context_uri": "spotify:playlist:066MaY4n6cAKnqWarv4kdF",
        "offset": {
            "position": 6
        },
        "position_ms": 0
    }
    body_json = json.dumps(body)
    yo = requests.put(url="https://api.spotify.com/v1/me/player/play", headers=headers, data=body_json)
    print(yo.text)
    print(yo)
    return redirect("/lyrics")


if __name__ == '__main__':
    app.run()