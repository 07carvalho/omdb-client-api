import string

from backend import test
from backend.exceptions import NotFound
from backend.models import movie
from backend.schemas.movie import MovieSchema
from backend.test.factories import create_movies


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

    def test_limit_offset_list_without_params(self):
        create_movies()

        instances = movie.Movie.limit_offset_list()

        self.assertEqual(len(instances), 10)
        self.assertEqual(instances[0].title, "Shark A")
        self.assertEqual(instances[9].title, "Shark J")

    def test_limit_offset_list_with_params(self):
        create_movies()

        values = [[0, 10, 10], [10, 20, 16], [20, 20, 6], [30, 10, 0]]
        for item in values:
            instances = movie.Movie.limit_offset_list(offset=item[0], limit=item[1])

            self.assertEqual(len(instances), item[2])
            if len(instances) > 0:
                self.assertEqual(
                    instances[0].title, f"Shark {string.ascii_uppercase[item[0]]}"
                )
                self.assertEqual(
                    instances[len(instances) - 1].title,
                    f"Shark {string.ascii_uppercase[item[0]+len(instances)-1]}",
                )

    def test_limit_offset_list_without_data(self):
        instances = movie.Movie.limit_offset_list()

        self.assertEqual(len(instances), 0)

    def test_filter_by_title(self):
        create_movies()

        instance = movie.Movie.filter_by("title", "Shark C")

        self.assertEqual(instance.title, "Shark C")
        self.assertEqual(instance.imdb_id, "tt2071492")
        self.assertEqual(instance.year, "2012")
        self.assertEqual(instance.poster, "https://poster.com/test2.png")

    def test_filter_by_imdb_title(self):
        create_movies()

        instance = movie.Movie.filter_by("imdb_id", "tt2071492")

        self.assertEqual(instance.title, "Shark C")
        self.assertEqual(instance.imdb_id, "tt2071492")
        self.assertEqual(instance.year, "2012")
        self.assertEqual(instance.poster, "https://poster.com/test2.png")

    def test_filter_by_invalid_field(self):
        create_movies()

        with self.assertRaises(AttributeError) as context:
            movie.Movie.filter_by("duration", "122")

            self.assertEqual(AttributeError, type(context.exception))

    def test_delete(self):
        obj = movie.Movie.create(
            title="Mega Shark vs. Giant Octopus",
            imdb_id="tt1350498",
            year="2009",
            poster="https://poster.com/test3.png",
        )

        movie.Movie.delete(obj.id)

        self.assertEqual(movie.Movie.count(), 0)
