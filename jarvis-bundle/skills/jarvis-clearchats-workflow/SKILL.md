---
name: jarvis-clearchats-workflow
description: >
  Safe deletion workflow for the Jarvis-clearchats subagent.
  Governs dry-run preview, user confirmation gate, and destructive execution.
---

# Jarvis-clearchats Workflow Skill

## Guardrails — Never Violate

- Never run the destructive command without first showing the dry-run output.
- Never skip user confirmation — not even if the user said "just do it".
- Never delete sessions newer than the threshold — the script enforces this, but verify the `--days` value before running.
- If VS Code is open, warn the user before any run. The SQLite database may be locked.
- The script creates a `.bak` backup automatically. Confirm the backup path in the final report.

## Step 1 — Parse the Request

Extract from the user's message:
- **Days threshold** (`--days N`): how old a session must be to be eligible for deletion. Default: **4**.
- **Mode**: is this a preview-only request ("dry run", "just show me", "preview")? If yes, stop after Step 3.

## Step 2 — Warn About VS Code Lock

Before running anything:

> If VS Code is currently open, the chat database may be locked by the application.
> The script will report a "database is locked" error if this happens.
> Close VS Code before running the destructive step, or the deletion will fail silently.

## Step 3 — Dry Run (Mandatory)

Always run the preview first:

```
python scripts/clear-old-chats.py --days {DAYS} --dry-run
```

Show the complete output to the user. The output lists every session that would be deleted.

If no sessions would be deleted, report that and stop — do not proceed to Step 4.

## Step 4 — Confirmation Gate

After showing the dry-run output, ask explicitly:

> The dry run identified **X sessions** older than **N days** that would be deleted.
> This action cannot be undone (though a backup will be saved automatically).
> **Confirm deletion? (yes / no)**

Do not proceed until the user responds affirmatively.

## Step 5 — Destructive Run

Only after explicit confirmation:

```
python scripts/clear-old-chats.py --days {DAYS}
```

## Step 6 — Delivery Report

```
## Chat Cleanup Complete

- Sessions deleted: X
- Days threshold: N days
- Backup saved at: <path reported by script>
```

If the script errors with a lock message, instruct the user to close VS Code and re-run from Step 3.
