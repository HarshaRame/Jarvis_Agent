---
name: jarvis-develop-workflow
description: >
  Implementation workflow for the Jarvis-develop subagent.
  Covers requirement validation, pre-implementation exploration, modular code standards,
  concurrency selection, AWS/AI integration patterns, and the delivery report format.
  Load when Jarvis-develop is building a new feature, applying fixes from a findings report,
  or implementing any change to a Python or PHP codebase.
---

# Jarvis-develop Workflow Skill

## Guardrails — Never Violate

- Never hardcode secrets, API keys, or passwords — source from `config/aws_config.py`, `.env`, or env vars.
- Never modify files outside the agreed SCOPE.
- Never add a new external dependency without stating why and confirming no existing utility covers the need.
- Never break backward compatibility unless explicitly required by the task.
- Never implement against ambiguous requirements — resolve them before writing a single line.
- Never skip the exploration step — reading existing code is not optional.

---

## Step 1 — Validate the Input

Before exploring the codebase:

**If input is a task description:**
- Identify: what to build, which files/modules are affected, expected inputs/outputs, constraints.
- Flag any real ambiguity — contradictions, missing key details, destructive scope.
- State all assumptions explicitly. Do not guess silently.

**If input is `test-findings.md`:**
- Read the full report.
- Separate findings by severity: implement [CRITICAL] and [HIGH] in full; flag [MEDIUM] and [LOW] as optional.
- Note any finding that conflicts with other findings or requires a design decision.
- List the files that will be touched before starting.

---

## Step 2 — Explore First

In this exact order:

1. Read config files — `config/aws_config.py`, `.env.example`, `settings.py` — understand what's available.
2. Read entry points — understand execution flow before touching internals.
3. Read the specific files in scope — understand existing patterns, naming, error handling style.
4. Check for existing utilities that might already solve part of the problem.
5. Check test files for the affected modules — understand expected behaviour.

**Rule**: If you find an existing utility that does 80% of what's needed, extend it — do not create a parallel implementation.

---

## Step 3 — Plan the Change

Before writing code, produce a plan:

```
Files to create: [list]
Files to modify: [list]
Files NOT to touch: [list]
Concurrency approach: [async / threading / multiprocessing / none — and why]
New dependencies: [list, or "none"]
Backward-compat impact: [describe or "none"]
```

The plan must be consistent with the existing architecture. If the plan requires a design departure, explain why and what the trade-off is.

---

## Step 4 — Concurrency Decision

Evaluate every loop and I/O-heavy operation against this table before implementing:

| Workload type | Preferred approach |
|---|---|
| HTTP calls, DB reads, file I/O (I/O-bound) | `asyncio` or `threading` with `ThreadPoolExecutor` |
| Data transforms, parsing, encoding (CPU-bound) | `multiprocessing` or `ProcessPoolExecutor` |
| Large dataset with independent rows | Batched processing with configurable `batch_size` |
| Mixed I/O + CPU pipeline | Thread pool for I/O stage, process pool for CPU stage |
| Low volume, sequential clearly sufficient | Keep it simple — no forced concurrency |

Document the concurrency choice in a comment at the top of the relevant function or module.

---

## Step 5 — Modularity Standards

Every implementation must follow:

- **One responsibility per function / class / module.** If a function does two things, split it.
- **Shared logic in utilities.** Never duplicate a helper across two files — extract it.
- **Config separated from logic.** Constants in a constants module; secrets in env/config; no inline magic values.
- **Thin entry points.** `main.py`, `run.php`, CLI handlers contain only: arg parsing, setup, and a single call into a module. Business logic lives in modules.
- **Folder structure by feature, not by file type.** `feature/service.py`, `feature/repository.py` — not `services/feature.py`, `repositories/feature.py`.

---

## Step 6 — AWS / AI Integration Patterns

Follow these exactly when writing Bedrock or Lambda code. Deviations require explicit justification.

### Bedrock — Client Setup
```python
import boto3
import json
from config import aws_config

client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=aws_config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=aws_config.AWS_SECRET_ACCESS_KEY,
    region_name=aws_config.AWS_REGION
)
```

### Bedrock — Invocation with Backoff
```python
import time

def invoke_bedrock(payload: dict, max_retries: int = 5) -> str:
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": payload["messages"],
        "max_tokens": payload.get("max_tokens", 1024),
        "temperature": payload.get("temperature", 0.3),
    })
    for attempt in range(max_retries):
        try:
            response = client.invoke_model(
                modelId=aws_config.BEDROCK_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=body
            )
            return json.loads(response["body"].read())["content"][0]["text"]
        except client.exceptions.ThrottlingException:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Bedrock — Image Message Format
```python
import base64, httpx

def image_to_bedrock_message(url: str) -> dict:
    raw = httpx.get(url).content
    media_type = _detect_media_type(raw)   # validate — never assume jpeg
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": base64.b64encode(raw).decode()
        }
    }
```

### Temperature Values
- Attribute detection / visual analysis: `0.3`
- Marketing copy / creative content: `0.4`–`0.7`
- Using the wrong temperature for the wrong task is a bug — not a style issue.

### Prompt Templates (Bedrock)
- Templates live in `apps/inspirational/configurations/`.
- Load with `LocalConfigLoader._load_text()` (`.txt`) or `_load_json()` (`.json`).
- Interpolate with `PromptBuilder.interpolate(template, data)` using `{{placeholder}}` syntax.
- Never build Bedrock prompts with f-strings — use `PromptBuilder`.

### Lambda — Synchronous Invocation
```python
lambda_client = boto3.client('lambda', region_name=aws_config.AWS_REGION)

def call_lambda(function_name: str, payload: dict) -> dict:
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload).encode()
    )
    return json.loads(response['Payload'].read())
```

---

## Step 7 — Pre-Delivery Quality Gate

Before reporting done, verify:

- [ ] All [CRITICAL] and [HIGH] findings from input addressed (or explicitly noted as skipped with reason)
- [ ] No new `import` of an external library added without justification in the report
- [ ] No hardcoded credential, key, or password in any changed file
- [ ] No syntax error — mentally trace the changed code or run a linter
- [ ] No logic that duplicates an existing utility
- [ ] Concurrency approach documented at the function/module level
- [ ] Entry points remain thin
- [ ] No files modified outside the agreed SCOPE

---

## Step 8 — Delivery Report

End every task with this report structure:

```
## Changes Made

### Created
- `path/to/new_file.py` — <one-line purpose>

### Modified
- `path/to/changed_file.py` — <what changed and why>

## Findings Addressed
| Finding | Severity | Status |
|---------|----------|--------|
| <title> | CRITICAL | Fixed |
| <title> | HIGH | Fixed |
| <title> | MEDIUM | Deferred — <reason> |

## Assumptions Made
- <assumption 1>
- <assumption 2>

## Follow-up Items
- <anything deferred, needs user decision, or requires a subsequent test run>
```
