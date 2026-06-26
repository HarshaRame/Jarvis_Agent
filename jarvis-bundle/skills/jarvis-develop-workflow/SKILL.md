---
name: jarvis-develop-workflow
description: >
  Implementation workflow for the Jarvis-develop subagent.
  Covers requirement validation, pre-implementation exploration, modular code standards,
  concurrency selection, AWS/AI integration patterns.
---

# Jarvis-develop Workflow Skill

## Guardrails — Never Violate

- Never hardcode secrets, API keys, or passwords — source from `config/aws_config.py`, `.env`, or env vars.
- Never modify files outside the agreed SCOPE.
- Never add a new external dependency without stating why and confirming no existing utility covers the need.
- Never break backward compatibility unless explicitly required by the task.
- Never implement against ambiguous requirements — resolve them before writing a single line.
- Never skip the exploration step — reading existing code is not optional.

## Step 1 — Validate the Input

**If input is a task description:**
- Identify: what to build, which files/modules are affected, expected inputs/outputs, constraints.
- Flag any real ambiguity — contradictions, missing key details, destructive scope.
- State all assumptions explicitly. Do not guess silently.

**If input is `test-findings.md`:**
- Read the full report.
- Separate findings by severity: implement [CRITICAL] and [HIGH] in full; flag [MEDIUM] and [LOW] as optional.
- Note any finding that conflicts with other findings or requires a design decision.
- List the files that will be touched before starting.

## Step 2 — Explore First

In this exact order:

1. Read config files — `config/aws_config.py`, `.env.example`, `settings.py` — understand what's available.
2. Read entry points — understand execution flow before touching internals.
3. Read the specific files in scope — understand existing patterns, naming, error handling style.
4. Check for existing utilities that might already solve part of the problem.
5. Check test files for the affected modules — understand expected behaviour.

**Rule**: If you find an existing utility that does 80% of what's needed, extend it — do not create a parallel implementation.

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

## Modularity Standards

- One responsibility per function / class / module
- Shared logic extracted into utilities — never duplicated
- Configuration separated from logic (config files, env vars, constants modules)
- Entry points (`main.py`, `run.php`, CLI handlers) kept thin — logic lives in modules
- Folder structure reflects feature boundaries, not file types

## Concurrency Decision Guide

| Workload Type | Preferred Approach |
|---|---|
| I/O-bound (HTTP, DB, file reads) | `asyncio` or `threading` |
| CPU-bound (data transforms, parsing) | `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` |
| Large datasets with independent rows | Batched processing with configurable batch size |
| Mixed I/O + CPU | Thread pool for I/O, process pool for CPU stages |
| Sequential is clearly sufficient | Keep it simple — no forced concurrency |
