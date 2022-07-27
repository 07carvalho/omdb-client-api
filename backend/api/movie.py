import random

from backend import api
from backend.exceptions import NotFound
from backend.models import movie
from backend.pagination import LimitOffsetPagination
from backend.swagger import swagger
from backend.wsgi import messages, remote


class GetRequest(messages.Message):
    title = messages.StringField(1)


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
    @swagger("Get a movie")
    @remote.method(GetRequest, MovieResponse)
    def get(self, request):
        if request.title:
            instance = movie.Movie.filter_by("title", request.title)
        else:
            instance = movie.Movie.limit_offset_list(
                random.randint(1, movie.Movie.count() - 1), 1
            )[0]

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
        instances = movie.Movie.limit_offset_list(offset, limit)
        return LimitOffsetPagination(
            serializer=ListResponse,
            instances=instances,
            offset=offset,
            limit=limit,
        ).get_pagination()
