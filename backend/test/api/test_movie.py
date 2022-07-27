import string

from backend import test
from backend.models import movie
from backend.schemas.movie import MovieSchema


class TestMovieApi(test.TestCase):
    def _create_bulk(self):
        movies = []
        chars = string.ascii_uppercase
        for i in range(len(chars)):
            movies.append(
                MovieSchema(
                    title=f"Shark {chars[i]}",
                    imdb_id=f"tt207149{i}",
                    year=f"201{i}",
                    poster=f"https://poster.com/test{i}.png",
                )
            )
        movie.Movie.bulk_create(movies)

    def test_list_without_params(self):
        self._create_bulk()

        resp = self.api_client.post("movie.list")

        self.assertEqual(resp.get("offset"), 0)
        self.assertEqual(resp.get("limit"), 10)

    def test_list_with_params(self):
        self._create_bulk()

        resp = self.api_client.post("movie.list", dict(offset=10, limit=20))

        self.assertEqual(resp.get("offset"), 10)
        self.assertEqual(resp.get("limit"), 20)
        self.assertEqual(len(resp.get("results")), 16)
