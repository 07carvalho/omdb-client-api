import os
import pkgutil
import time

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
        start_time = time.time()
        print("No movie in the database. Please wait while we prepare everything...")
        MovieService.populate_database()
        print(
            f"Done! The database was populated with {Movie.count()} movies in {'{:.3f}'.format(time.time() - start_time)} seconds!"
        )


def message_to_dict(request):
    keys = [key for key in request.all_keys()]
    result = dict()
    for key in keys:
        result[key] = getattr(request, key)
    return result


for _, modname, _ in pkgutil.walk_packages(
    path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + "."
):
    __import__(modname)
