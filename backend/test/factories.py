import string

from backend.models import movie
from backend.schemas.movie import MovieSchema


def create_user_and_get_access_token(client):
    resp = client.post(
        "user.create", dict(name="test", email="test@gmail.com", password="test")
    )
    return resp.get("access_token")


def create_movies():
    movies = []
    chars = string.ascii_uppercase
    for i in range(len(chars)):
        movies.append(
            MovieSchema(
                title=f"Shark {chars[i]}",
                imdb_id=f"tt207149{i}",
                year=f"201{i}",
                poster=f"https://poster.com/test{i}.png",
            )
        )
    return movie.Movie.bulk_create(movies)
