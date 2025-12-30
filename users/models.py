from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # faqat sinf kerak dedingiz
    grade = models.PositiveSmallIntegerField("Sinf", default=1)

    def __str__(self) -> str:
        return f"{self.username} (sinf: {self.grade})"
