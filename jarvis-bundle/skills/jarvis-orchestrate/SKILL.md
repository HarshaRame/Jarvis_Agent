---
name: jarvis-orchestrate
description: >
  Orchestration skill for the Jarvis agent. Covers task planning, specialist routing,
  delegation format, multi-agent chaining, and output verification.
---

# Jarvis Orchestration Skill

## Phase 1 — Understand Before Acting

Before touching any tool or delegating:

1. **Read the request completely.** Identify: scope, target files/features, desired output, any constraints.
2. **Classify ambiguity level:**
   - **Real ambiguity** (contradictory requirements, missing key detail, destructive risk) → ask one focused question before proceeding.
   - **Resolvable assumption** (reasonable default exists) → state the assumption, proceed.
3. **Do not delegate until the requirement is clear.** Partial clarity leads to wasted subagent work.

## Phase 2 — Routing Decision

Apply the first matching rule:

| User signal | Route to |
|---|---|
| "test", "audit", "find bugs", "review for errors", "check", "what's broken" | **Jarvis-test** |
| "build", "implement", "create", "fix", "develop", "write code", "add feature" | **Jarvis-develop** |
| "document", "README", "setup guide", "docstrings", "API reference", "changelog" | **Jarvis-docs** |
| "clear chats", "clean up chat history", "delete old sessions" | **Jarvis-clearchats** |
| "test and fix", "find and fix", "full cycle", "end to end" | **Jarvis-test → Jarvis-develop** (chained) |
| "test, fix, and document" | **Jarvis-test → Jarvis-develop → Jarvis-docs** (chained) |
| New feature with unclear requirements | Clarify first, then **Jarvis-develop** |

## Phase 3 — Delegation Format

Every subagent invocation must include all five fields:

```
TASK: <one-sentence description of exactly what to do>
SCOPE: <list of files, directories, or features in scope>
INPUT: <path to findings file, requirement doc, or "none">
OUTPUT: <expected deliverable — file path, report, or summary>
CONSTRAINTS: <anything not to touch, backward-compat requirements, known risks>
```

Incomplete delegations are the primary cause of subagent errors. Never omit SCOPE or CONSTRAINTS.

## Phase 4 — Multi-Agent Chaining

For full-cycle workflows, pass output explicitly between agents:

```
Step 1: Jarvis-test → OUTPUT: test-findings.md
Step 2: Jarvis-develop → INPUT: test-findings.md
Step 3 (optional): Jarvis-test re-run → SCOPE: only files changed
Step 4 (optional): Jarvis-docs → INPUT: changes summary
```

Do not skip steps or merge them.
