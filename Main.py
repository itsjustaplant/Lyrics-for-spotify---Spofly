from flask import Flask, render_template, redirect, request
import requests
import json
import base64
from bs4 import BeautifulSoup


app = Flask(__name__)
TOKEN = " "
CLIENT_ID = "e6cd36c6ea1c44b09245097b9e3367e1"
CLIENT_SECRET = "94c8b9efa0f34440b7c3225b75ff0b37"
GENIUS_URL = "http://www.genius.com/"


@app.route("/")
def log():
    return redirect(
                    "https://accounts.spotify.com/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost:5000/callback&scope=user-read-currently-playing")


@app.route("/callback")
def token():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": "http://localhost:5000/callback",
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    base = "{}:{}"
    format_client = base.format(CLIENT_ID, CLIENT_SECRET)
    base64encoded = base64.urlsafe_b64encode(format_client.encode()).decode()
    headers = {
        "Authorization": "Basic {}".format(base64encoded)
    }
    post_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    global TOKEN
    TOKEN = access_token
    return redirect("/lyrics")


@app.route("/lyrics")
def init():
    spotify = requests.get("https://api.spotify.com/v1/me/player/currently_playing?access_token=" + TOKEN)
    
    current_song = spotify.json()
    song_title = current_song['item']['name']
    artist_name = current_song['item']['artists'][0]['name']
    image_url = current_song['item']['album']['images'][0]['url']
    duration_ms = current_song['item']['duration_ms']
    progress_ms = current_song['progress_ms']
    refresh_ms = (duration_ms - progress_ms) / 1000 - 15
    
    if refresh_ms < 0:
        refresh_ms *= -1
    
    quote = "'"
    artist_name_edited=json.dumps(artist_name).replace(' ','-').replace('"','',2).replace(quote,'')
    song_title_edited=json.dumps(song_title).replace(' ','-').replace('"','',2).replace(quote,'').replace('(','').replace(')','')
    song_url = GENIUS_URL+artist_name_edited+"-"+song_title_edited+"-lyrics"
    data = requests.get(song_url)
    print(song_url)
    if data.status_code==404:
        lyrics = "lyrics not found"

    else:
        
        soup = BeautifulSoup(data.text,"html.parser")
        lyrics = soup.find("div",attrs={'class':'lyrics'})
        lyrics = lyrics.get_text()
        lyrics=lyrics[2::]
        """
            lyricsgenius can be used
            song = genius.search_song(title=song_title, artist=artist_name)
            song_lyrics = song.lyrics
            
            """

    return render_template("home.html", data=lyrics, artist_name=artist_name, song_title=song_title,
                       image=image_url, refresh_ms=refresh_ms)
if __name__ == '__main__':
    app.run()

