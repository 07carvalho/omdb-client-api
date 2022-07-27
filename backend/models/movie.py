from typing import List

from google.cloud import ndb

from backend.models import base
from backend.schemas.movie import MovieSchema


class Movie(base.BaseModel):
    title = ndb.StringProperty(indexed=True)
    imdb_id = ndb.StringProperty(indexed=True)
    year = ndb.StringProperty()
    poster = ndb.StringProperty()
    normalized_name = ndb.ComputedProperty(
        lambda self: self.title and self.title.lower(), indexed=True
    )

    @classmethod
    def bulk_create(cls, movies: List[MovieSchema]):
        instances = [
            cls(
                title=movie.title,
                imdb_id=movie.imdb_id,
                year=movie.year,
                poster=movie.poster,
            )
            for movie in movies
        ]
        return ndb.put_multi(instances)

    @classmethod
    def limit_offset_list(cls, offset=0, limit=10):
        return cls.query().order(cls.title).fetch(offset=offset, limit=limit)
