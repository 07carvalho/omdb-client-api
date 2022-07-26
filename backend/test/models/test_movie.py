from backend import test
from backend.exceptions import NotFound
from backend.models import movie
from backend.schemas.movie import MovieSchema


class TestMovie(test.TestCase):
    def test_create(self):
        obj = movie.Movie.create(
            title="Shark Tale",
            imdb_id="tt0307453",
            year="2004",
            poster="https://poster.com/test.png",
        )

        self.assertTrue(obj.title == "Shark Tale")
        self.assertTrue(obj.imdb_id == "tt0307453")
        self.assertTrue(obj.year == "2004")
        self.assertTrue(obj.poster == "https://poster.com/test.png")

    def test_bulk_create(self):
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

        obj = movie.Movie.bulk_create(movies)

        self.assertEqual(len(obj), len(movies))
        self.assertEqual(movie.Movie.count(), len(movies))

    def test_get(self):
        obj = movie.Movie.create(
            title="Mega Shark vs. Giant Octopus",
            imdb_id="tt1350498",
            year="2009",
            poster="https://poster.com/test3.png",
        )

        instance = movie.Movie.get(obj.id)

        self.assertEqual(obj, instance)

    def test_movie_not_found(self):
        with self.assertRaises(NotFound) as context:
            movie.Movie.get("agRzdHVicgoLEgRVc2VyGAEM")

        self.assertEqual(NotFound, type(context.exception))
