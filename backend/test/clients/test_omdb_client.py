from unittest.mock import patch

from omdb import OMDBClient as OMDBClientLib

from backend import test
from backend.clients.omdb import OMDbClient
from backend.exceptions import NotFound
from backend.schemas.movie import MovieSchema


class TestOMDbClient(test.TestCase):
    def test_get_by_title(self):
        movie = {
            "title": "Jurassic Shark",
            "imdb_id": "tt2071491",
            "year": "2012",
            "poster": "https://poster.com/test1.png",
        }

        with patch.object(OMDBClientLib, "title", return_value=movie) as mock_method:
            response = OMDbClient().get_by_title("title")

            mock_method.assert_called_once_with("title")
            self.assertEqual(type(response), MovieSchema)
            self.assertEqual(response.title, "Jurassic Shark")
            self.assertEqual(response.imdb_id, "tt2071491")
            self.assertEqual(response.year, "2012")
            self.assertEqual(response.poster, "https://poster.com/test1.png")

    def test_get_by_title_not_found(self):
        movie = {}

        with patch.object(OMDBClientLib, "title", return_value=movie) as mock_method:
            with self.assertRaises(NotFound) as context:
                OMDbClient().get_by_title("title")

                mock_method.assert_called_once_with("title")
                self.assertEqual(NotFound, type(context.exception))

    def test_search_movie(self):
        movies = [
            {
                "title": "Jurassic Shark",
                "imdb_id": "tt2071491",
                "year": "2012",
                "poster": "https://poster.com/test1.png",
            },
            {
                "title": "Ghost Shark",
                "imdb_id": "tt2600742",
                "year": "2013",
                "poster": "https://poster.com/test2.png",
            },
        ]

        with patch.object(
            OMDBClientLib, "search_movie", return_value=movies
        ) as mock_method:
            response = OMDbClient().search_movie("query")

            mock_method.assert_called_once_with(string="query", page=1)
            self.assertEqual(len(response), len(movies))

    def test_search_movie_not_found(self):
        movies = []

        with patch.object(
            OMDBClientLib, "search_movie", return_value=movies
        ) as mock_method:
            with self.assertRaises(NotFound) as context:
                OMDbClient().search_movie("query")

                mock_method.assert_called_once_with(string="query", page=1)
                self.assertEqual(NotFound, type(context.exception))
