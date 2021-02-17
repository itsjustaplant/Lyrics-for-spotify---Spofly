import os

from flask import Flask, render_template, redirect, session

import services

app = Flask(__name__)
app.secret_key = os.urandom(20)


@app.route("/")
def landing():
    return render_template("login.html")


@app.route("/login")
def login():
    return redirect(services.login())


@app.route("/callback")
def callback():
    services.callback()
    return redirect("/lyrics")


@app.route("/lyrics")
def lyrics():
    song, artist, refresh_ms, is_local, artwork_url = services.get_song()
    bg_color, txt_color = services.get_colors(is_local, artwork_url)
    song_lyrics = services.get_lyrics(artist, song)
    return render_template("lyrics.html", artwork_url=artwork_url, artist_name=artist, song_name=song, data=song_lyrics,
                           refresh_ms=refresh_ms, bg=bg_color, fg=txt_color)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run()
