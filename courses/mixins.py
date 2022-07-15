class SerializerByRoleMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(
            self.request.user.is_teacher, self.serializer_class
        )
