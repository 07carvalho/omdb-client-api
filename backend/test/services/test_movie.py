from unittest.mock import patch

from backend import test
from backend.clients.omdb import OMDbClient
from backend.models import movie
from backend.schemas.movie import MovieSchema
from backend.services.movie import MovieService


class TestMovie(test.TestCase):
    def test_populate_database(self):
        movies = [
            MovieSchema(
                title="Jurassic Shark",
                imdb_id="tt2071491",
                year="2012",
                poster="https://poster.com/test1.png",
            ),
            MovieSchema(
                title="Ghost Shark",
                imdb_id="tt2600742",
                year="2013",
                poster="https://poster.com/test2.png",
            ),
        ]

        with patch.object(
            OMDbClient, "search_movie", return_value=movies
        ) as mock_method:
            obj = MovieService.populate_database()

            self.assertEqual(mock_method.call_count, 10)
            self.assertEqual(len(obj), len(movies * 10))
            self.assertEqual(len(obj), movie.Movie.count())
