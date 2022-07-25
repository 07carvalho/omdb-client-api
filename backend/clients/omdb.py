from decouple import config
from omdb import OMDBClient

from backend import error
from backend.schemas.movie import MovieSchema


class MovieNotFound(error.Error):
    pass


class OMDbClient:
    def __init__(self):
        self.client = OMDBClient(apikey=config("OMDB_APIKEY"))

    def get_by_title(self, title: str) -> MovieSchema:
        result = self.client.title(title)
        if not result:
            raise MovieNotFound()
        return MovieSchema(
            title=result.get("title"),
            imdb_id=result.get("Title"),
            year=result.get("year"),
            poster=result.get("poster"),
        )

    def search_movie(self, query: str, page=1):
        result = self.client.search_movie(string=query, page=page)
        if not result:
            raise MovieNotFound()
        return [
            MovieSchema(
                title=movie.get("title"),
                imdb_id=movie.get("Title"),
                year=movie.get("year"),
                poster=movie.get("poster"),
            )
            for movie in result
        ]
