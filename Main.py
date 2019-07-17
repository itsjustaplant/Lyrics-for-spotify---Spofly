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
                    "https://accounts.spotify.com/authorize?client_id=e6cd36c6ea1c44b09245097b9e3367e1&response_type=code&redirect_uri=https://spoflyv1.herokuapp.com/callback&scope=user-read-currently-playing")


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
    access_token = response_data['access_token']
    global TOKEN
    TOKEN = access_token
    return redirect("/lyrics")


@app.route("/lyrics")
def init():
    return "a"
if __name__ == '__main__':
    app.run()

