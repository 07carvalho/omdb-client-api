from backend import api
from backend.clients.omdb import OMDbClient
from backend.exceptions import NotFound
from backend.models import movie
from backend.oauth2 import oauth2
from backend.pagination import LimitOffsetPagination
from backend.swagger import swagger
from backend.wsgi import messages, remote
from backend.wsgi.protorpc import message_types


class CreateRequest(messages.Message):
    title = messages.StringField(1, required=True)


class DeleteRequest(messages.Message):
    id = messages.StringField(1, required=True)


class GetRequest(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)


class ListRequest(messages.Message):
    offset = messages.IntegerField(1)
    limit = messages.IntegerField(2)


class MovieResponse(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)
    imdb_id = messages.StringField(3)
    year = messages.StringField(4)
    poster = messages.StringField(5)


class ListResponse(messages.Message):
    offset = messages.IntegerField(1)
    limit = messages.IntegerField(2)
    results = messages.MessageField(MovieResponse, 3, repeated=True)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Create a movie")
    @remote.method(CreateRequest, MovieResponse)
    def create(self, request):
        try:
            response = OMDbClient().get_by_title(request.title)
        except NotFound:
            raise NotFound(message="Movie not found in IMDb")

        instance = movie.Movie.create(
            title=response.title,
            imdb_id=response.imdb_id,
            year=response.year,
            poster=response.poster,
        )

        return MovieResponse(
            id=instance.id,
            title=response.title,
            imdb_id=response.imdb_id,
            year=response.year,
            poster=response.poster,
        )

    @swagger("Get a movie")
    @remote.method(GetRequest, MovieResponse)
    def get(self, request):
        instance = None
        if movie_id := request.id:
            instance = movie.Movie.get(movie_id)
        elif title := request.title:
            instance = movie.Movie.filter_by("title", title)

        if instance is None:
            raise NotFound(message="Movie not found")

        return MovieResponse(
            id=instance.id,
            title=instance.title,
            imdb_id=instance.imdb_id,
            year=instance.year,
            poster=instance.poster,
        )

    @swagger("List movies")
    @remote.method(ListRequest, ListResponse)
    def list(self, request):
        offset = request.offset or 0
        limit = request.limit or 10
        entities = movie.Movie.limit_offset_list(offset, limit)
        return LimitOffsetPagination(
            serializer=ListResponse,
            entities=entities,
            offset=offset,
            limit=limit,
        ).get_pagination()

    @swagger("Delete movie")
    @oauth2.required()
    @remote.method(DeleteRequest, message_types.VoidMessage)
    def delete(self, request):
        movie.Movie.delete(request.id)
        return message_types.VoidMessage()
