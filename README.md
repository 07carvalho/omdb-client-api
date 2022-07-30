# omdb-client-api
![Test Coverage](coverage-badge.svg)

## Running the project:

### Start the backend:
```
export OMDB_APIKEY=<omdb_key>
gunicorn backend.gunicorn:application
```

### Run tests:
```
python test.py
```

### Show test coverage:
```
python test.py -c
```

### Suggestions for improvements
- refactor tests to use `pytest` and reduce duplicate code with `fixtures`
- use caching to improve API response time
- use `poetry` to manage dependencies
- wrap everything with docker
- update, clean and add tests to `backend/wsgi`
