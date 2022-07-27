from backend import api
from backend.models import movie
from backend.pagination import LimitOffsetPagination
from backend.swagger import swagger
from backend.wsgi import messages, remote


class ListRequest(messages.Message):
    offset = messages.IntegerField(1)
    limit = messages.IntegerField(2)


class MovieResponse(messages.Message):
    title = messages.StringField(1)
    imdb_id = messages.StringField(2)
    year = messages.StringField(3)
    poster = messages.StringField(4)


class ListResponse(messages.Message):
    offset = messages.IntegerField(1)
    limit = messages.IntegerField(2)
    results = messages.MessageField(MovieResponse, 3, repeated=True)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
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
