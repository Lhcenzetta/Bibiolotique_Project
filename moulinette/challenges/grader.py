import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .models import Exercise, TestCase


@dataclass
class TestResult:
    passed: bool
    input_text: str
    expected_output_text: str
    actual_output_text: str
    error_text: str
    runtime_ms: int


def run_python_code_against_tests(code: str, tests: List[TestCase], time_limit_ms: int) -> Tuple[int, List[TestResult]]:
    results: List[TestResult] = []
    total_score = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        program_path = Path(tmpdir) / "solution.py"
        program_path.write_text(code)

        for test in tests:
            try:
                proc = subprocess.run(
                    [sys.executable, str(program_path)],
                    input=(test.input_text or ""),
                    capture_output=True,
                    text=True,
                    timeout=max(0.001, time_limit_ms / 1000.0),
                )
                stdout = proc.stdout.rstrip("\n")
                stderr = proc.stderr
                passed = stdout == (test.expected_output_text.rstrip("\n")) and proc.returncode == 0
                runtime_ms = 0  # basic placeholder
            except subprocess.TimeoutExpired as ex:
                stdout = ex.stdout or ""
                stderr = "TIMEOUT"
                passed = False
                runtime_ms = time_limit_ms

            if passed:
                total_score += test.weight

            results.append(
                TestResult(
                    passed=passed,
                    input_text=test.input_text,
                    expected_output_text=test.expected_output_text,
                    actual_output_text=stdout,
                    error_text=stderr,
                    runtime_ms=runtime_ms,
                )
            )

    return total_score, results
