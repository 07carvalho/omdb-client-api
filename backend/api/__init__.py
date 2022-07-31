import pkgutil

from backend import wsgi


class Application(wsgi.Application):
    pass


application = Application(base_path="api")
service = application.service
endpoint = application.service


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
