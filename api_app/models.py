import uuid
from django.db import models
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL


class QueryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.TextField()
    answer = models.TextField(blank=True)
    top_score = models.FloatField(default=0.0)
    chunks = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Feedback(models.Model):
    CHOICES = (("up", "up"), ("down", "down"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query_log = models.ForeignKey(QueryLog, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.CharField(max_length=10, choices=CHOICES)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
