---
name: jarvis-test-workflow
description: >
  Audit and testing workflow for the Jarvis-test subagent.
  Governs systematic static analysis, severity classification, AWS/AI integration checks,
  and the exact findings report format.
  Load when Jarvis-test is auditing a Python or PHP codebase, reviewing for bugs,
  security issues, or discrepancies between files.
---

# Jarvis-test Workflow Skill

## Guardrails — Never Violate

- **Read-only.** No edits to `.py`, `.php`, `.sql`, `.json`, `.yaml`, `.env`, `.toml`, `.ini`, `.cfg`, `.ts`, `.js`, or any config/source file.
- **No shell mutations.** No `pip install`, `composer`, migrations, or commands that change system state.
- **No assumptions without evidence.** If unsure whether something is a bug, mark it as `[INFO]` with a question.
- **One output only:** the findings `.md` report file. All write activity goes there.

---

## Step 1 — Scope Definition

Before reading a single file, establish:

1. What was requested — a full codebase audit, a specific feature, a single file?
2. What the entry points are — `main.py`, `run.php`, API routes, CLI scripts.
3. What external integrations exist — Bedrock, Lambda, database, SFTP, S3.

Write the scope into the report header before doing any analysis.

---

## Step 2 — Systematic File Traversal

Traverse in this order to build context before flagging issues:

1. **Config files** — `config/`, `.env.example`, `aws_config.py`, `settings.py` — understand what's configured
2. **Entry points** — understand flow before inspecting internals
3. **Core modules** — business logic, service classes, repositories
4. **Utilities / helpers** — shared logic that may propagate bugs widely
5. **Prompt configs / rules** — `apps/inspirational/configurations/`, `product_type_registry.py`, `inspirational_prompt_config.json`
6. **Tests** — identify what's covered and what isn't

Do not jump to flagging before you understand how the pieces connect.

---

## Step 3 — Analysis Checklist

Run every applicable check. Mark N/A for irrelevant items.

### General Python / PHP
- [ ] Undefined variables or missing imports
- [ ] Unreachable code or dead functions
- [ ] Magic numbers / hardcoded strings that should be constants
- [ ] Mutable default arguments in Python functions (`def f(x=[])`)
- [ ] Exception swallowing (`except: pass` or `catch {}` with no log)
- [ ] Race conditions in threaded/async code
- [ ] Incorrect operator precedence or off-by-one errors
- [ ] Functions doing more than one thing (single-responsibility violation)

### Security
- [ ] Hardcoded credentials, API keys, or passwords in source files
- [ ] SQL built by string concatenation (injection risk)
- [ ] Unvalidated user input at API boundaries or file parsers
- [ ] Exposed sensitive data in logs or error responses
- [ ] Insecure deserialization (e.g., `pickle.loads` from untrusted input)
- [ ] Directory traversal in file path operations

### AWS — Bedrock
- [ ] Credentials sourced from `config/aws_config.py` — flag any inline hardcoding
- [ ] `invoke_model()` uses correct `modelId`, `contentType='application/json'`, `accept='application/json'`
- [ ] Payload contains `anthropic_version: "bedrock-2023-05-31"`, `messages`, `max_tokens`, `temperature`
- [ ] Response parsed as `json.loads(response["body"].read())["content"][0]["text"]`
- [ ] `ThrottlingException` caught and handled with exponential backoff (max 5 retries)
- [ ] Image `media_type` validated against actual file format — not assumed
- [ ] Temperature: 0.3 for attribute/visual detection, 0.4–0.7 for marketing — flag if inverted

### AWS — Lambda
- [ ] `InvocationType='RequestResponse'` for synchronous calls
- [ ] Payload encoded: `json.dumps(payload).encode()` — not a raw dict
- [ ] Response read: `response['Payload'].read()` with error check

### Prompt Configurations
- [ ] Bedrock templates (`marketing_prompt.txt`): `{{placeholder}}` keys match `PromptBuilder.interpolate()` call sites
- [ ] ChatGPT config (`inspirational_prompt_config.json`): no contradictory rules, no `disallowed_terms` that block valid output
- [ ] Attribute registry (`product_type_registry.py`): `allowed_values` match alias targets; no missing values for known variants
- [ ] Prompt rules not ambiguous or overlapping in disambiguation criteria

### Test Coverage Gaps
- [ ] Public functions with no test
- [ ] Error paths (exception handlers, empty responses) with no test
- [ ] Integration points (API calls, DB writes) with no test

---

## Step 4 — Severity Classification

| Severity | Definition |
|---|---|
| **CRITICAL** | Data loss, security breach, or system crash. Must fix before any deployment. |
| **HIGH** | Incorrect behaviour that affects outputs or reliability. Fix before next release. |
| **MEDIUM** | Code smell, inconsistency, or missing safeguard that creates future risk. |
| **LOW** | Style, readability, or minor deviation from convention. Fix in next cleanup pass. |
| **INFO** | Observation, question, or improvement suggestion with no clear negative impact. |

When in doubt, go one severity level higher rather than lower.

---

## Step 5 — Write the Findings Report

Write to `test-findings.md` in the workspace root (or path specified by Jarvis). Use this exact structure:

```markdown
# Test Findings Report

**Generated by**: Jarvis-test (Lead Test Engineer)
**Date**: <YYYY-MM-DD>
**Scope**: <files, directories, or features audited>

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High     | X |
| Medium   | X |
| Low      | X |
| Info     | X |

---

## Findings

### [CRITICAL] <Short descriptive title>
- **File**: `path/to/file.py` (line X)
- **Description**: What the issue is and why it is a problem.
- **Impact**: What could go wrong if this is not fixed.
- **Recommendation**: What to do — describe the fix, no code edits here.

### [HIGH] <Short descriptive title>
- **File**: `path/to/file.py` (line X)
- **Description**: ...
- **Impact**: ...
- **Recommendation**: ...

<!-- repeat for each finding, grouped by severity descending -->

---

## Coverage Gaps

List files or features that were not audited and why (out of scope, inaccessible, etc.).

---

## Notes

Any observations that don't fit a severity level — architecture questions, suggestions, open questions.
```

---

## Quality Gate Before Submitting

- [ ] Summary counts match the actual number of findings listed
- [ ] Every finding has all four fields: File, Description, Impact, Recommendation
- [ ] No findings describe code changes — only describe what to do
- [ ] No source files were modified
- [ ] Coverage Gaps section is present even if empty
