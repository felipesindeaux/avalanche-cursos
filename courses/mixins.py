class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        if self.request.auth:
            if self.request.user.is_teacher:
                return self.serializer_map.get('Teacher')
            return self.serializer_map.get('Student')
        return self.serializer_map.get('Teacher')
