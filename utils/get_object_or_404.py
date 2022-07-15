from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


def get_object_or_404(model, detail="Not found", **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        raise NotFound(detail)
