from unittest.mock import patch

from omdb import OMDBClient

from backend import test
from backend.models import movie
from backend.test.factories import create_movies


class TestMovieApi(test.TestCase):
    def test_list_without_params(self):
        create_movies()

        resp = self.api_client.post("movie.list")

        self.assertEqual(resp.get("offset"), 0)
        self.assertEqual(resp.get("limit"), 10)

    def test_list_with_params(self):
        create_movies()

        resp = self.api_client.post("movie.list", dict(offset=10, limit=20))

        self.assertEqual(resp.get("offset"), 10)
        self.assertEqual(resp.get("limit"), 20)
        self.assertEqual(len(resp.get("results")), 16)

    def test_list_with_wrong_offset(self):
        resp = self.api_client.post("movie.list", dict(offset="A", limit=10))

        self.assertEqual(resp.get("error").get("code"), "400 Bad Request")

    def test_list_with_wrong_limit(self):
        resp = self.api_client.post("movie.list", dict(offset=0, limit="A"))

        self.assertEqual(resp.get("error").get("code"), "400 Bad Request")

    def test_get_a_movie(self):
        create_movies()

        resp = self.api_client.post("movie.get")

        self.assertTrue("id" in resp)
        self.assertTrue("title" in resp)
        self.assertTrue("imdb_id" in resp)
        self.assertTrue("year" in resp)
        self.assertTrue("poster" in resp)

    def test_get_by_title(self):
        create_movies()

        resp = self.api_client.post("movie.get", dict(title="Shark Z"))

        self.assertEqual(resp.get("title"), "Shark Z")
        self.assertEqual(resp.get("imdb_id"), "tt20714925")
        self.assertEqual(resp.get("year"), "20125")
        self.assertEqual(resp.get("poster"), "https://poster.com/test25.png")

    def test_get_by_title_not_found(self):
        create_movies()

        resp = self.api_client.post("movie.get", dict(title="Shark ABC"))

        self.assertEqual(resp.get("error").get("message"), "Movie not found")

    def test_create_movie(self):
        count = movie.Movie.count()
        title = "Mega Shark - The return of the drowned"
        data = {
            "title": title,
            "imdb_id": "tt123",
            "year": "2022",
            "poster": "https://localhost:8000/teste.png",
        }

        with patch.object(OMDBClient, "title", return_value=data) as mock_method:
            resp = self.api_client.post("movie.create", dict(title=title))

            mock_method.assert_called_once_with(title)
            self.assertEqual(count + 1, movie.Movie.count())
            self.assertEqual(resp.get("title"), title)
            self.assertEqual(resp.get("imdb_id"), "tt123")
            self.assertEqual(resp.get("year"), "2022")
            self.assertEqual(resp.get("poster"), "https://localhost:8000/teste.png")

    def test_create_movie_not_found(self):
        count = movie.Movie.count()
        title = "Sharks are bad"

        with patch.object(OMDBClient, "title", return_value={}) as mock_method:
            resp = self.api_client.post("movie.create", dict(title=title))

            mock_method.assert_called_once_with(title)
            self.assertEqual(count, movie.Movie.count())
            self.assertEqual(
                resp.get("error").get("message"), "Movie not found in IMDb"
            )

    def test_delete_authorized_user(self):
        instance = movie.Movie.create(
            title="Mega Shark vs. Giant Octopus",
            imdb_id="tt1350498",
            year="2009",
            poster="https://poster.com/test3.png",
        )
        self.assertEqual(movie.Movie.count(), 1)
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")

        resp = self.api_client.post(
            "movie.delete",
            dict(id=instance.id),
            headers=dict(authorization=access_token),
        )

        self.assertEqual(movie.Movie.count(), 0)
        self.assertEqual(resp, {})

    def test_delete_not_authorized_user(self):
        resp = self.api_client.post("movie.delete", dict(id="abcAsgd"))

        self.assertEqual(
            resp.get("error").get("message"), "Invalid or expired access token"
        )
        self.assertEqual(resp.get("error").get("error_name"), "Unauthorized")
