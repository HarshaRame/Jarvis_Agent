---
name: jarvis-docs-workflow
description: >
  Documentation workflow for the Jarvis-docs subagent.
  Governs which documents to produce, the README standard structure, per-section rules,
  docstring format, and the accuracy-first verification process.
  Load when Jarvis-docs is creating, updating, or auditing any documentation for a Python
  or PHP project — README, setup guide, API reference, docstrings, or changelogs.
---

# Jarvis-docs Workflow Skill

## Guardrails — Never Violate

- Never describe behaviour that isn't verified in the source code. Read the code first.
- Never invent function signatures, environment variables, or configuration keys — find them in the files.
- Never modify source code logic — only documentation files, docstrings, and inline comments.
- Never produce a document with placeholder text like "TODO" or "TBD" — if something is genuinely unknown, say "Not documented. Check with the project maintainer." explicitly.
- Every command in every document must be complete, copy-pasteable, and tested against the actual codebase.

---

## Step 1 — Read Before Writing

Before writing a single line of documentation:

1. Read the entry point files (`main.py`, `run.php`, CLI scripts) to understand execution flow.
2. Read config files (`.env.example`, `aws_config.py`, `settings.py`) to find all env vars and settings.
3. Read `requirements.txt` / `composer.json` to find actual dependencies and versions.
4. Read the test files to understand expected behaviour and edge cases.
5. Identify any existing documentation to understand what already exists and what needs updating.

---

## Step 2 — Decide What to Produce

Match the task to the right document type:

| Situation | Produce |
|---|---|
| New project or missing entry doc | `README.md` |
| Non-trivial install with env setup | `SETUP.md` |
| HTTP API or library with public interface | `API.md` |
| Multi-step pipeline or automation workflow | `WORKFLOWS.md` |
| Test suite instructions missing or outdated | `TESTING.md` |
| Release with user-facing changes | `CHANGELOG.md` entry |
| Python function/class with non-obvious logic | Inline docstring |
| PHP / Python logic block that needs explanation | Inline comment |

When asked to "update docs", identify which of the above are stale before writing.

---

## Step 3 — README.md Standard

Every README must contain these sections in this order:

```markdown
# <Project Name>

> <One sentence: what this does and why it exists.>

## Table of Contents
## Overview
## Prerequisites
## Installation
## Configuration
## Usage
## How to Run
## How to Test
## Project Structure
## API Reference        ← include only if project exposes an API
## Troubleshooting
## Contributing         ← include only if relevant
## License              ← include only if relevant
```

**Section rules:**

### Prerequisites
- Exact versions: `Python 3.11+`, `PHP 8.2+`, `MySQL 8.0+`
- OS constraints if any
- External services or credentials required

### Installation
- Numbered step-by-step list
- Every command is complete — no `...` or implied steps
- Python: include venv creation and activation
- PHP: include `composer install`

### Configuration
- Table of every environment variable:

  | Variable | Description | Example | Required |
  |---|---|---|---|
  | `AWS_ACCESS_KEY_ID` | AWS access key | `AKIA...` | Yes |

- Show a `.env.example` block
- Never include real values

### How to Run
- Separate subsections for: development, production, background/scheduled processes
- Exact command with all required arguments
- Expected output or success indicator

### How to Test
- Command to run full test suite
- Command to run a single test or test file
- Command to run with coverage report

### Project Structure
- Tree of top-level directories with one-line descriptions
- Only top two levels unless structure is flat

---

## Step 4 — API Reference Standard

For every endpoint, document:

```markdown
### POST /endpoint-path

**Description**: What this endpoint does.

**Request Body**:
| Field | Type | Required | Description |
|---|---|---|---|
| `field_name` | string | Yes | What it is |

**Response** (`200 OK`):
```json
{
  "key": "value"
}
```

**Error Responses**:
| Code | Condition |
|---|---|
| `400` | Missing required field |
| `500` | Internal error |
```

---

## Step 5 — Python Docstring Format

Use Google-style docstrings for all Python functions and classes:

```python
def function_name(param1: str, param2: int) -> dict:
    """One-line summary ending with a period.

    Longer description only if the logic is non-obvious. Skip if
    the one-liner is sufficient.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of the returned value and its structure.

    Raises:
        ValueError: When param1 is empty.
        ThrottlingException: When Bedrock rate limit is hit.
    """
```

Rules:
- One-liner is mandatory. Extended description is optional.
- Do not add docstrings to trivial getters or one-liners that are self-explanatory.
- Do not describe what the code does line by line — describe what it does and why.

---

## Step 6 — Inline Comment Rules

Use inline comments only for:
- Non-obvious algorithmic decisions ("exponential backoff: base 2, max 5 retries")
- Business rules embedded in code ("temperature 0.3 = precision mode per product spec")
- Known gotchas or warnings ("media_type must be validated — Bedrock rejects mismatched types")

Do not comment on code that is self-describing. `# increment counter` above `count += 1` is noise.

---

## Step 7 — Accuracy Verification Checklist

Before submitting any documentation:

- [ ] Every environment variable listed in docs was found in the actual config/env files
- [ ] Every command was traced to confirm it matches the actual entry point and args
- [ ] Every function signature in API docs was read directly from the source file
- [ ] No section contains "TODO", "TBD", or placeholder text
- [ ] No real credentials appear anywhere in the documentation
- [ ] Project Structure tree reflects the actual folder layout
- [ ] Test commands produce the output described

---

## Step 8 — Delivery Report

End every docs task with:

```
## Documents Produced / Updated

| File | Action | Sections Changed |
|------|--------|-----------------|
| `README.md` | Created | All |
| `API.md` | Updated | POST /generate-copy |

## Source Files Read
- <list of files read to produce the documentation>

## Known Gaps
- <anything that couldn't be documented because the source was unclear or missing>
```
