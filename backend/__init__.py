import os
import time

from backend.gunicorn import ndb_client
from backend.models.movie import Movie
from backend.services.movie import MovieService

with ndb_client.context():
    if Movie.count() == 0 and os.getenv("ENV") != "test":
        start_time = time.time()
        print("No movie in the database. Please wait while we prepare everything...")
        MovieService.populate_database()
        print(
            f"Done! The database was populated with {Movie.count()} movies in {'{:.3f}'.format(time.time() - start_time)} seconds!"
        )
