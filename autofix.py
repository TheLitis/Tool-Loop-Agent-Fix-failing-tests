import argparse
import re
import subprocess
import sys
from pathlib import Path


PATCH_RULES = {
    "test_subtract_basic": (
        "def subtract(a, b):\n    # Intentional bug for autofix demo.\n    return a + b",
        "def subtract(a, b):\n    # Intentional bug for autofix demo.\n    return a - b",
    ),
    "test_divide_returns_float": (
        "def divide(a, b):\n    if b == 0:\n        raise ValueError(\"division by zero\")\n    # Intentional bug for autofix demo.\n    return a // b",
        "def divide(a, b):\n    if b == 0:\n        raise ValueError(\"division by zero\")\n    # Intentional bug for autofix demo.\n    return a / b",
    ),
}


def run_pytest():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    if output:
        print(output)
    return result.returncode, output


def parse_failed_tests(output):
    return set(re.findall(r"FAILED\s+\S+::(test_[a-zA-Z0-9_]+)", output))


def apply_hardcoded_patches(failed_tests):
    file_path = Path("calculator.py")
    source = file_path.read_text(encoding="utf-8")
    updated = source
    applied = []

    for test_name in sorted(failed_tests):
        rule = PATCH_RULES.get(test_name)
        if not rule:
            continue
        old_snippet, new_snippet = rule
        if old_snippet in updated:
            updated = updated.replace(old_snippet, new_snippet, 1)
            applied.append(test_name)

    if applied and updated != source:
        file_path.write_text(updated, encoding="utf-8")

    return applied


def autofix(max_iterations):
    for iteration in range(1, max_iterations + 1):
        print(f"FAIL: running pytest (iteration {iteration}/{max_iterations})")
        code, output = run_pytest()
        if code == 0:
            print("PASS: all tests are green")
            return 0

        failed_tests = parse_failed_tests(output)
        if not failed_tests:
            print("PATCH: no parsable failed tests, stopping")
            return 1

        applied = apply_hardcoded_patches(failed_tests)
        if not applied:
            print("PATCH: no applicable hardcoded patches, stopping")
            return 1

        print("PATCH: applied fixes for " + ", ".join(applied))

    print("FAIL: max iterations reached without full pass")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Autofix pytest failures with hardcoded patches.")
    parser.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args()
    raise SystemExit(autofix(max_iterations=args.max_iterations))


if __name__ == "__main__":
    main()
