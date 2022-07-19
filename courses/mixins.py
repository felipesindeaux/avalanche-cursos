class SerializerByUserRoleMixin:
    def get_serializer_class(self, *args, **kwargs):
        if self.request.auth:
            if self.request.user.is_teacher:
                return self.serializer_map.get("Teacher")
            return self.serializer_map.get("Student")
        return self.serializer_map.get("Teacher")


class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)
