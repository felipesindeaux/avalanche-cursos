from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.


class Review(models.Model):
    score   = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user    = models.ForeignKey("users.User", on_delete=models.DO_NOTHING, related_name="reviews")
    course  = models.ForeignKey("courses.Course", on_delete=models.DO_NOTHING, related_name="reviews")