from django.db import models

from django.db import models

class Answer(models.Model):

    answer = models.CharField(max_length=255)
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, related_name="answers")

