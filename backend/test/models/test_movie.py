import string

from backend import test
from backend.exceptions import NotFound
from backend.models import movie
from backend.schemas.movie import MovieSchema


class TestMovie(test.TestCase):
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
        self._create_bulk()

        instances = movie.Movie.limit_offset_list()

        self.assertEqual(len(instances), 10)
        self.assertEqual(instances[0].title, "Shark A")
        self.assertEqual(instances[9].title, "Shark J")

    def test_limit_offset_list_with_params(self):
        self._create_bulk()

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
