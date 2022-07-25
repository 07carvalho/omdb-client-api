import os
import pkgutil

from google.cloud import ndb

from backend import wsgi
from backend.models.movie import Movie
from backend.services.movie import MovieService

ndb_client = ndb.Client()


class Application(wsgi.Application):
    pass


application = Application(base_path="api")
service = application.service
endpoint = application.service

with ndb_client.context():
    if Movie.count() == 0 and os.getenv("ENV") != "test":
        print("No movie in the database. Please wait while we prepare everything...")
        MovieService.populate_database()
        print(f"Done! The database was populated with {Movie.count()} movies!")

for _, modname, _ in pkgutil.walk_packages(
    path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + "."
):
    __import__(modname)
