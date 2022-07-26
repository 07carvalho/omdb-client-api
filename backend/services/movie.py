from backend.clients.omdb import OMDbClient
from backend.models.movie import Movie


class MovieService:
    @staticmethod
    def populate_database():
        movies = []
        for page in range(1, 11):
            movies_per_page = OMDbClient().search_movie(query="shark", page=page)
            movies.extend(movies_per_page)
        return Movie.bulk_create(movies)
