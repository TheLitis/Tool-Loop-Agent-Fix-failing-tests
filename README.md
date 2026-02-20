# Tool-Loop-Agent-Fix-failing-tests

Mini demo repository for the workflow:
`Fail -> Patch -> Pass`

## Project layout

- `calculator.py` - calculator functions with bugs fixed by `autofix.py`
- `tests/test_calculator.py` - 5 pytest tests
- `autofix.py` - loop runner that parses pytest traceback and applies hardcoded patches
- `gallery/` - logs and media artifacts

## Reproduce FAIL (2 failed, 3 passed)

Restore the intentionally buggy calculator from the failing commit and run tests:

```powershell
git show 79a4f77:calculator.py > calculator.py
pytest -q
```

Expected result:

```text
2 failed, 3 passed
```

## Run autofix (FAIL -> PATCH -> PASS)

```powershell
python autofix.py
```

Expected output includes stage markers:

```text
FAIL
PATCH
PASS
```

## Verify PASS

```powershell
pytest -q
```

Expected result:

```text
5 passed
```

## Gallery artifacts

- `gallery/fail.png`
- `gallery/patch.png`
- `gallery/pass.png`
- `gallery/workflow_30s.gif` (30 seconds, 3 frames x 10 seconds)
