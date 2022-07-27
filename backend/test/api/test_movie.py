from backend import test
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
