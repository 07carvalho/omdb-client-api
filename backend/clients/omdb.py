import os
from typing import List

from omdb import OMDBClient

from backend.exceptions import NotFound
from backend.schemas.movie import MovieSchema


class OMDbClient:
    def __init__(self):
        self.client = OMDBClient(apikey=os.getenv("OMDB_APIKEY"))

    def get_by_title(self, title: str) -> MovieSchema:
        result = self.client.title(title)
        if not result:
            raise NotFound("Movie not found")
        return MovieSchema(
            title=result.get("title"),
            imdb_id=result.get("imdb_id"),
            year=result.get("year"),
            poster=result.get("poster"),
        )

    def search_movie(self, query: str, page=1) -> List[MovieSchema]:
        result = self.client.search_movie(string=query, page=page)
        if not result:
            raise NotFound("Movie not found")
        return [
            MovieSchema(
                title=movie.get("title"),
                imdb_id=movie.get("imdb_id"),
                year=movie.get("year"),
                poster=movie.get("poster"),
            )
            for movie in result
        ]
