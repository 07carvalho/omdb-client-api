from backend import test
from backend.models import movie
from backend.services.movie import MovieService


class TestMovie(test.TestCase):
    def test_populate_database(self):
        obj = MovieService.populate_database()

        self.assertEqual(len(obj), movie.Movie.count())
