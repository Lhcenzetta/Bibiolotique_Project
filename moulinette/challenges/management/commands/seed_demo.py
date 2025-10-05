from django.core.management.base import BaseCommand
from challenges.models import Exercise, TestCase


class Command(BaseCommand):
    help = "Seed demo exercises and tests"

    def handle(self, *args, **options):
        ex, _ = Exercise.objects.get_or_create(
            slug="sum-two-ints",
            defaults={
                "title": "Sum two integers",
                "description": "Read two integers and print their sum.",
                "starter_code": "a,b=map(int,input().split())\nprint(a+b)\n",
                "time_limit_ms": 1500,
                "is_active": True,
            },
        )
        TestCase.objects.get_or_create(
            exercise=ex,
            input_text="1 2\n",
            expected_output_text="3",
            defaults={"is_public": True, "weight": 1},
        )
        TestCase.objects.get_or_create(
            exercise=ex,
            input_text="-5 5\n",
            expected_output_text="0",
            defaults={"is_public": False, "weight": 1},
        )
        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
