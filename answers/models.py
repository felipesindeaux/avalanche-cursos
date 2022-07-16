from django.db import models
import uuid


class Answer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    answer = models.CharField(max_length=255)
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="answers")

