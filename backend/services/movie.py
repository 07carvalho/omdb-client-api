from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

from backend.clients.omdb import OMDbClient
from backend.models import movie


class MovieService:
    @staticmethod
    def populate_database():
        movies = []
        pages = [page for page in range(1, 11)]
        with ThreadPoolExecutor(max_workers=10) as pool:
            search_movie = OMDbClient().search_movie
            # yes, just shark movies
            for i in pool.map(search_movie, repeat("shark"), pages):
                movies.extend(i)
        return movie.Movie.bulk_create(movies)
