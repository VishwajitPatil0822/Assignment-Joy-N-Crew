from django.db import models

class Choice(models.Model):
    ROUND_TYPES = [
        ("moment", "Moment"),
        ("evening", "Evening"),
        ("pace", "Pace"),
    ]

    round_number = models.PositiveSmallIntegerField()
    label = models.CharField(max_length=160)
    title = models.CharField(max_length=180)
    body = models.TextField()
    image_url = models.URLField(blank=True)
    profile_weights = models.JSONField(default=dict)
    round_type = models.CharField(max_length=20, choices=ROUND_TYPES, default="moment")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("round_number", "id")

    def __str__(self):
        return f"Round {self.round_number} — {self.title}"


class ChoiceSession(models.Model):
    session_key = models.CharField(max_length=64, unique=True)
    choices = models.JSONField(default=list)
    profile = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_key
