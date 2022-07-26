from google.cloud import ndb

from backend import error


class NotFound(error.Error):
    pass


class BaseModel(ndb.Model):
    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def get(cls, instance_id):
        instance = ndb.Key(urlsafe=instance_id).get()

        if instance is None or not isinstance(instance, cls):
            raise NotFound(f"No instance found with id: {instance_id}")
        return instance

    @property
    def id(self):
        return self.key.urlsafe().decode("utf-8")

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))
