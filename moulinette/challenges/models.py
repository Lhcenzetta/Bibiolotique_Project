from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Exercise(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    starter_code = models.TextField(blank=True)
    time_limit_ms = models.PositiveIntegerField(default=2000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title}"


class TestCase(models.Model):
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="test_cases"
    )
    input_text = models.TextField(blank=True)
    expected_output_text = models.TextField()
    is_public = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:  # pragma: no cover
        return f"TestCase({self.exercise.slug} #{self.pk})"


class Submission(models.Model):
    STATUS_PASSED = "PASSED"
    STATUS_FAILED = "FAILED"
    STATUS_ERROR = "ERROR"
    STATUS_CHOICES = [
        (STATUS_PASSED, "Passed"),
        (STATUS_FAILED, "Failed"),
        (STATUS_ERROR, "Error"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    code = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    score = models.IntegerField(default=0)
    detail_json = models.JSONField(default=dict)
    runtime_ms = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "exercise", "status"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"Submission({self.user.username}, {self.exercise.slug}, {self.status})"


# Create your models here.
