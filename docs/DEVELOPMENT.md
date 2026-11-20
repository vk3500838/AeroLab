# Development workflow

## Set up

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -e ".[dev]"
```

## Quality gates

Before committing:

```bash
pytest --cov=aerolab
ruff check src tests
```

## Branch and commit practice

Use a small feature branch for each coherent change:

```bash
git switch -c feature/campaign-comparison
# implement + tests
git add src tests docs
git commit -m "Add campaign comparison statistics"
```

Do not create commits that claim work you did not perform. Commit after a feature is implemented and tested. Keep generated reports out of source control unless they are intentionally included as documented examples.

## Engineering change checklist

- Are all inputs and outputs in documented units?
- Are invalid and boundary cases handled?
- Are assumptions and equations documented?
- Are there tests for nominal, boundary, and failure cases?
- Does the CLI provide an actionable error?
- Can another person reproduce the result from a clean environment?
