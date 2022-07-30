from backend.exceptions import PaginationFieldMissingOrInvalid


class LimitOffsetPagination:
    def __init__(self, serializer, entities, offset: int, limit: int):
        self.serializer = serializer
        self.entities = entities
        self.offset = offset
        self.limit = limit

    def get_pagination(self):
        return self.serializer(
            offset=self.get_offset(),
            limit=self.get_limit(),
            results=self.serialize_data(),
        )

    def get_offset(self):
        if type(self.offset) != int or self.offset < 0:
            raise PaginationFieldMissingOrInvalid(
                "Offset must be zero or a positive integer"
            )
        return self.offset

    def get_limit(self):
        if type(self.limit) != int or self.limit < 0:
            raise PaginationFieldMissingOrInvalid("Limit must be a positive integer")
        return self.limit

    def serialize_data(self):
        results = []
        if len(self.entities) == 0:
            return results

        try:
            result_field_class = self.serializer.field_by_name("results")
        except KeyError:
            raise KeyError("Response should have 'results' field")
        instance_message_class = result_field_class.message_type
        keys = [key for key in instance_message_class().all_keys()]
        for instance in self.entities:
            obj = instance_message_class()
            for key in keys:
                setattr(obj, key, getattr(instance, key))
            results.append(obj)
        return results
