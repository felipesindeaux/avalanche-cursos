import uuid

from rest_framework.exceptions import ValidationError


def validate_uuid(str):

    try:
        validated_uuid = uuid.UUID(str)
        return validated_uuid
    except ValueError:
        raise ValidationError({"detail": "Invalid UUID param"})
