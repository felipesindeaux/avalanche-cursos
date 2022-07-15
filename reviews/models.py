from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="reviews"
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.DO_NOTHING, related_name="reviews"
    )
