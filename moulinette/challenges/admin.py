from django.contrib import admin
from .models import Exercise, TestCase, Submission


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "time_limit_ms")
    list_filter = ("is_active",)
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("exercise", "is_public", "weight")
    list_filter = ("exercise", "is_public")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "exercise", "status", "score", "runtime_ms", "created_at")
    list_filter = ("status", "exercise")
    search_fields = ("user__username", "exercise__slug")

# Register your models here.
