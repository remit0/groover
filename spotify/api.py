import base64
import json
import os
from datetime import timedelta

import requests
from django.utils import timezone

from spotify.models import SpotifyToken, Album, Artist


class SpotifyAuth(object):

    SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
    SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CALLBACK_URL = "http://localhost:5000/auth"
    SCOPE = "user-read-email user-read-private"

    def getAuth(self, client_id, redirect_uri, scope):
        return (
            f"{self.SPOTIFY_URL_AUTH}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
        )

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }
        post = requests.post(self.SPOTIFY_URL_TOKEN, params=body, headers=headers)
        return self.handleToken(json.loads(post.text))

    def handleToken(self, response):
        if "error" in response:
            return response
        return {
            key: response[key]
            for key in ["access_token", "expires_in", "refresh_token"]
        }

    def handleRefreshToken(self, response):
        if "error" in response:
            return response
        return {
            key: response[key]
            for key in ["access_token", "expires_in"]
        }

    def refreshAuth(self, refresh_token):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        encoded = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }
        post_refresh = requests.post(
            self.SPOTIFY_URL_TOKEN, data=body, headers=headers
        )
        return self.handleRefreshToken(json.loads(post_refresh.text))

    def getUser(self):
        return self.getAuth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )

    def getUserToken(self, code):
        return self.getToken(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )


class SpotifyRequest:

    def __init__(self):
        token = SpotifyToken.objects.last()
        if not token.is_valid():
            self.refresh_token(token)
        self.headers = {"Authorization": f"Bearer {token.token}"}

    @staticmethod
    def refresh_token(token):
        auth = SpotifyAuth()
        response = auth.refreshAuth(token.refresh_token)
        token.token = response["access_token"]
        token.expiry_date = timezone.now() + timedelta(seconds=response["expires_in"])
        token.save()

    def make_request(self, url):
        return requests.get(url, headers=self.headers)

    def get_new_releases(self):
        url = "https://api.spotify.com/v1/browse/new-releases"
        response = self.make_request(url)
        if response.status_code == 200:
            response = json.loads(response.text)
            self.persist_new_release_call(response)

    def persist_new_release_call(self, response):
        for album_data in response["albums"]["items"]:
            album = Album.from_response(album_data)
            album.save()
            for artist_data in album_data["artists"]:
                artist = Artist.from_reponse(artist_data)
                artist.save()
                album.artists.add(artist)
