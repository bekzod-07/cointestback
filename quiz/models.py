# quiz/models.py
from django.conf import settings
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    class CorrectChoice(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"

    grade = models.PositiveSmallIntegerField("Sinf")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )

    text = models.TextField("Savol matni")

    option_a = models.CharField("Variant A", max_length=255)
    option_b = models.CharField("Variant B", max_length=255)
    option_c = models.CharField("Variant C", max_length=255)
    option_d = models.CharField("Variant D", max_length=255)

    correct = models.CharField(
        "To‘g‘ri javob", max_length=1, choices=CorrectChoice.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["grade"]),
            models.Index(fields=["subject"]),
        ]

    def __str__(self) -> str:
        return f"[{self.grade}] {self.subject}: {self.text[:40]}"


class TestAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attempts"
    )
    grade = models.PositiveSmallIntegerField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attempts",
    )

    total = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong = models.PositiveIntegerField(default=0)

    # ✅ YANGI: test yechishga ketgan vaqt (sekund)
    duration_seconds = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["grade", "subject"]),
            models.Index(fields=["correct", "duration_seconds", "created_at"]),
        ]

    def __str__(self) -> str:
        return (
            f"{self.user.username} | {self.grade} | {self.subject} | "
            f"{self.correct}/{self.total} | {self.duration_seconds}s"
        )


class TestAnswer(models.Model):
    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)  # A/B/C/D
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Test javobi"
        verbose_name_plural = "Test javoblari"
        unique_together = ("attempt", "question")
        indexes = [
            models.Index(fields=["attempt"]),
            models.Index(fields=["question"]),
            models.Index(fields=["is_correct"]),
        ]

    def __str__(self) -> str:
        return f"Attempt#{self.attempt_id} Q#{self.question_id} {self.selected} ({self.is_correct})"
