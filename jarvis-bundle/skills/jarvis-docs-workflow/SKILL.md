---
name: jarvis-docs-workflow
description: >
  Documentation workflow for the Jarvis-docs subagent.
  Governs which documents to produce, the README standard structure, per-section rules,
  docstring format, and the accuracy-first verification process.
---

# Jarvis-docs Workflow Skill

## Guardrails — Never Violate

- Never describe behaviour that isn't verified in the source code. Read the code first.
- Never invent function signatures, environment variables, or configuration keys — find them in the files.
- Never modify source code logic — only documentation files, docstrings, and inline comments.
- Never produce a document with placeholder text like "TODO" or "TBD"
- Every command in every document must be complete, copy-pasteable, and tested against actual codebase.

## Step 1 — Read Before Writing

Before writing a single line of documentation:

1. Read the entry point files (`main.py`, `run.php`, CLI scripts) to understand execution flow.
2. Read config files (`.env.example`, `aws_config.py`, `settings.py`) to find all env vars and settings.
3. Read `requirements.txt` / `composer.json` to find actual dependencies and versions.
4. Read the test files to understand expected behaviour and edge cases.
5. Identify any existing documentation to understand what already exists.

## Step 2 — Decide What to Produce

Match the task to the right document type:

| Situation | Produce |
|---|---|
| New project or missing entry doc | `README.md` |
| Non-trivial install with env setup | `SETUP.md` |
| HTTP API or library with public interface | `API.md` |
| Multi-step pipeline or automation workflow | `WORKFLOWS.md` |
| Test suite instructions missing | `TESTING.md` |
| Release with user-facing changes | `CHANGELOG.md` entry |
| Python function/class with non-obvious logic | Inline docstring |
| PHP / Python logic block that needs explanation | Inline comment |

## Step 3 — README.md Standard Structure

Every README must contain these sections:

```markdown
# <Project Name>

> One-sentence: what this does and why it exists.

## Table of Contents
## Overview
## Prerequisites
## Installation
## Configuration
## Usage
## How to Run
## How to Test
## Project Structure
## API Reference (if applicable)
## Troubleshooting
## Contributing (if applicable)
## License (if applicable)
```

### Section Rules

- **Prerequisites**: Exact versions (`Python 3.11+`, `PHP 8.2+`, `MySQL 8.0+`)
- **Installation**: Numbered steps, every command complete, include venv/composer
- **Configuration**: Every environment variable in a table, show `.env.example` block
- **How to Run**: Separate subsections for development/production/background processes
- **How to Test**: Command to run full tests, single test, with coverage

## Python Docstring Standard (Google style)

```python
def process_records(records: list[dict], batch_size: int = 100) -> list[dict]:
    """Process a list of records in batches.

    Args:
        records: List of raw record dictionaries from the source system.
        batch_size: Number of records to process per batch. Defaults to 100.

    Returns:
        List of processed and validated record dictionaries.

    Raises:
        ValueError: If records is empty or batch_size is less than 1.
    """
```
