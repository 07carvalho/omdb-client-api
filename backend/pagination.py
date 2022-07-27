class LimitOffsetPagination:
    def __init__(self, serializer, instances, offset: int, limit: int):
        self.serializer = serializer
        self.instances = instances
        self.limit = limit
        self.offset = offset

    def get_pagination(self):
        return self.serializer(
            limit=self.limit,
            offset=self.offset,
            results=self.serialize_data(),
        )

    def serialize_data(self):
        results = []
        if len(self.instances) == 0:
            return results

        try:
            result_field_class = self.serializer.field_by_name("results")
        except KeyError:
            raise "Response should have 'results' field"
        instance_message_class = result_field_class.message_type
        keys = [key for key in instance_message_class().all_keys()]
        for instance in self.instances:
            obj = instance_message_class()
            for key in keys:
                setattr(obj, key, getattr(instance, key))
            results.append(obj)
        return results
