from backend import test
from backend.api.movie import MovieResponse
from backend.exceptions import PaginationFieldMissingOrInvalid
from backend.models import movie
from backend.pagination import LimitOffsetPagination
from backend.test.factories import create_movies
from backend.wsgi.protorpc import messages


class TestPagination(test.TestCase):
    def test_pagination(self):
        create_movies()
        entities = movie.Movie.limit_offset_list()

        class ListResponse(messages.Message):
            offset = messages.IntegerField(1)
            limit = messages.IntegerField(2)
            results = messages.MessageField(MovieResponse, 3, repeated=True)

        pagination = LimitOffsetPagination(
            serializer=ListResponse,
            entities=entities,
            offset=0,
            limit=10,
        ).get_pagination()

        self.assertEqual(type(pagination), ListResponse)
        self.assertEqual(pagination.offset, 0)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(len(pagination.results), len(entities))
        self.assertTrue(all([type(i) == MovieResponse for i in pagination.results]))

    def test_pagination_serializer_invalid(self):
        create_movies()
        entities = movie.Movie.limit_offset_list()

        class ListResponse(messages.Message):
            offset = messages.IntegerField(1)
            limit = messages.IntegerField(2)

        with self.assertRaises(KeyError) as context:
            LimitOffsetPagination(
                serializer=ListResponse,
                entities=entities,
                offset=0,
                limit=10,
            ).get_pagination()

            self.assertEqual(KeyError, type(context.exception))

    def test_invalid_offset(self):
        create_movies()
        entities = movie.Movie.limit_offset_list()

        class ListResponse(messages.Message):
            offset = messages.IntegerField(1)
            limit = messages.IntegerField(2)
            results = messages.MessageField(MovieResponse, 3, repeated=True)

        with self.assertRaises(PaginationFieldMissingOrInvalid) as context:
            LimitOffsetPagination(
                serializer=ListResponse,
                entities=entities,
                offset="A",
                limit=10,
            ).get_pagination()

            self.assertEqual(PaginationFieldMissingOrInvalid, type(context.exception))

    def test_invalid_limit(self):
        create_movies()
        entities = movie.Movie.limit_offset_list()

        class NewResponse(messages.Message):
            offset = messages.IntegerField(1)
            limit = messages.IntegerField(2)
            results = messages.MessageField(MovieResponse, 3, repeated=True)

        with self.assertRaises(PaginationFieldMissingOrInvalid) as context:
            LimitOffsetPagination(
                serializer=NewResponse,
                entities=entities,
                offset=10,
                limit="X",
            ).get_pagination()

            self.assertEqual(PaginationFieldMissingOrInvalid, type(context.exception))

    def test_empty_instance(self):
        class NewResponse(messages.Message):
            offset = messages.IntegerField(1)
            limit = messages.IntegerField(2)
            results = messages.MessageField(MovieResponse, 3, repeated=True)

        pagination = LimitOffsetPagination(
            serializer=NewResponse,
            entities=[],
            offset=10,
            limit=10,
        ).get_pagination()

        self.assertEqual(type(pagination), NewResponse)
        self.assertEqual(pagination.offset, 10)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(len(pagination.results), 0)
