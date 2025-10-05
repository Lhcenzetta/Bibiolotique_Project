from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Exercise, Submission
from .grader import run_python_code_against_tests


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("exam")
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def exam(request: HttpRequest) -> HttpResponse:
    exercise = Exercise.objects.filter(is_active=True).order_by("title").first()
    last_submission = None
    if exercise and request.user.is_authenticated:
        last_submission = (
            Submission.objects.filter(user=request.user, exercise=exercise).first()
        )
    return render(
        request,
        "exam.html",
        {
            "exercise": exercise,
            "last_submission": last_submission,
        },
    )


@login_required
@require_http_methods(["POST"])
def submit(request: HttpRequest) -> HttpResponse:
    code = request.POST.get("code", "")
    exercise_id = request.POST.get("exercise_id")
    exercise = Exercise.objects.get(id=exercise_id)

    tests = list(exercise.test_cases.all())
    total_weight = sum(t.weight for t in tests) or 1
    score, results = run_python_code_against_tests(
        code=code, tests=tests, time_limit_ms=exercise.time_limit_ms
    )

    status = Submission.STATUS_PASSED if score == total_weight else Submission.STATUS_FAILED
    detail = {
        "cases": [r.__dict__ for r in results],
        "total_weight": total_weight,
        "earned": score,
    }

    submission = Submission.objects.create(
        user=request.user,
        exercise=exercise,
        code=code,
        status=status,
        score=score,
        detail_json=detail,
    )
    return redirect("result", submission_id=submission.id)


@login_required
def result(request: HttpRequest, submission_id: int) -> HttpResponse:
    submission = Submission.objects.get(id=submission_id, user=request.user)
    return render(request, "result.html", {"submission": submission})


def leaderboard(request: HttpRequest) -> HttpResponse:
    rows = (
        Submission.objects.filter(status=Submission.STATUS_PASSED)
        .values("user__username")
        .annotate(total_score=Sum("score"))
        .order_by("-total_score", "user__username")
    )
    return render(request, "leaderboard.html", {"rows": rows})

# Create your views here.
