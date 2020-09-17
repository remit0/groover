from datetime import timedelta, datetime

from django.db import models
from django.utils import timezone


class SpotifyToken(models.Model):
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    refresh_token = models.CharField(max_length=500)

    @classmethod
    def from_reponse(cls, response):
        token = response["access_token"]
        refresh_token = response["refresh_token"]
        expires_in = response["expires_in"]
        expiry_date = timezone.now() + timedelta(seconds=expires_in)
        return cls(token=token, refresh_token=refresh_token, expiry_date=expiry_date)

    def is_valid(self):
        return timezone.now() < self.expiry_date


class Artist(models.Model):
    id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)

    @classmethod
    def from_reponse(cls, response):
        id = response["id"]
        name = response["name"]
        return cls(id, name)


class Album(models.Model):
    id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)
    date = models.DateField()
    artists = models.ManyToManyField(Artist)

    @classmethod
    def from_response(cls, response):
        id = response["id"]
        name = response["name"]
        date = datetime.strptime(response["release_date"], "%Y-%m-%d").date()
        return cls(id, name, date)
