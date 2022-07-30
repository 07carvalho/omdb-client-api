from google.cloud import ndb

from backend.exceptions import NotFound


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

    @classmethod
    def count(cls) -> int:
        return cls.query().count()

    @classmethod
    def filter_by(cls, field: str, query: str):
        try:
            model_field = getattr(cls, field)
        except AttributeError:
            raise AttributeError("Field does not exists in this model")
        entities = cls.query(model_field == query).fetch(1)
        return entities[0] if entities else None

    @property
    def id(self):
        return self.key.urlsafe().decode("utf-8")

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))
