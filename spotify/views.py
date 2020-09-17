from datetime import date

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .api import SpotifyAuth, SpotifyRequest
from .models import SpotifyToken, Album
from .serializers import ArtistSerializer
from .utils import remove_duplicates


@api_view(["GET"])
def get_authorization_code(request):
    params = request.query_params.dict()
    code = params.get("code", None)
    if code is None:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    else:
        auth = SpotifyAuth()
        token_response = auth.getUserToken(code)
        token = SpotifyToken.from_response(token_response)
        token.save()
        return Response(request.data)


@api_view(["GET"])
def get_artists(request):
    current_date = date.today()
    latest_album_date = Album.objects.latest("date").date
    if current_date > latest_album_date:
        api = SpotifyRequest()
        api.get_new_releases()
    latest_albums = Album.objects.all().order_by("date")[:10]
    artists = list()
    for album in latest_albums:
        artists += list(album.artists.all())
    artists = remove_duplicates(artists, "id")
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
