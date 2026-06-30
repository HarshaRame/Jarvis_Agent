"""
Switch between GitHub Copilot Chat and Amazon Q Developer in VS Code.
Only one assistant is active at a time. The inactive one is disabled.

Usage:
    python ai-switch.py [copilot|amazonq|status]

    copilot  — enable GitHub Copilot, disable Amazon Q
    amazonq  — enable Amazon Q, disable GitHub Copilot
    status   — show which assistant is currently active (default)

Requires VS Code window reload after switching.

NOTE: VS Code reads extensionsEnablement from state.vscdb at startup.
      After switching, reload the VS Code window (Ctrl+Shift+P > Reload Window).
      This script is OS-agnostic and works on Windows, macOS, and Linux.
"""

import sqlite3
import json
import shutil
import os
import sys
import platform
import argparse
from datetime import datetime

# Determine OS-specific paths
if platform.system() == "Windows":
    DB_PATH = os.path.join(
        os.environ.get("APPDATA", os.path.expanduser("~")),
        "Code", "User", "globalStorage", "state.vscdb"
    )
    STATE_FILE = os.path.join(
        os.environ.get("APPDATA", os.path.expanduser("~")),
        "Code", "User", "ai-switch.state"
    )
else:  # macOS and Linux
    DB_PATH = os.path.expanduser(
        "~/.config/Code/User/globalStorage/state.vscdb"
    )
    STATE_FILE = os.path.expanduser(
        "~/.config/Code/User/ai-switch.state"
    )
ENABLEMENT_KEY = "extensionsEnablement"

# Extension IDs
COPILOT_IDS = ["GitHub.copilot", "GitHub.copilot-chat"]
AMAZONQ_IDS = ["amazonwebservices.amazon-q-vscode"]

BANNER_COPILOT = """
╔══════════════════════════════════════════════╗
║   ✓  GitHub Copilot Chat  →  ACTIVE          ║
║   ✗  Amazon Q Developer   →  DISABLED        ║
╚══════════════════════════════════════════════╝
  Reload the VS Code window to apply: Ctrl+Shift+P > Reload Window
"""

BANNER_AMAZONQ = """
╔══════════════════════════════════════════════╗
║   ✗  GitHub Copilot Chat  →  DISABLED        ║
║   ✓  Amazon Q Developer   →  ACTIVE          ║
╚══════════════════════════════════════════════╝
  Reload the VS Code window to apply: Ctrl+Shift+P > Reload Window
"""


def read_state() -> str:
    """Return 'copilot' | 'amazonq' | 'unknown'."""
    if os.path.exists(STATE_FILE):
        try:
            return open(STATE_FILE).read().strip()
        except Exception:
            pass
    return "unknown"


def write_state(active: str) -> None:
    try:
        with open(STATE_FILE, "w") as f:
            f.write(active)
    except Exception as e:
        print(f"[WARN] Could not save state: {e}")


def read_enablement(cur: sqlite3.Cursor) -> list:
    cur.execute("SELECT value FROM ItemTable WHERE key = ?", (ENABLEMENT_KEY,))
    row = cur.fetchone()
    if not row or not row[0]:
        return []
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return []


def write_enablement(cur: sqlite3.Cursor, disabled: list) -> None:
    value = json.dumps(disabled, separators=(",", ":"))
    cur.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        (ENABLEMENT_KEY, value)
    )


def get_status():
    state = read_state()
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cur = conn.cursor()
        disabled = read_enablement(cur)
        conn.close()
    except Exception:
        disabled = []

    copilot_disabled = any(e in disabled for e in COPILOT_IDS)
    amazonq_disabled = any(e in disabled for e in AMAZONQ_IDS)

    print("── AI Assistant Status ──────────────────────────────")
    print(f"  GitHub Copilot Chat : {'DISABLED' if copilot_disabled else 'ENABLED'}")
    print(f"  Amazon Q Developer  : {'DISABLED' if amazonq_disabled else 'ENABLED'}")
    if state != "unknown":
        print(f"  Last switch target  : {state}")
    print("─────────────────────────────────────────────────────")

    if copilot_disabled and not amazonq_disabled:
        print("\n  Active: Amazon Q Developer")
    elif amazonq_disabled and not copilot_disabled:
        print("\n  Active: GitHub Copilot Chat")
    elif not copilot_disabled and not amazonq_disabled:
        print("\n  WARNING: Both are currently ENABLED. Run 'ai-switch.py copilot' or 'ai-switch.py amazonq' to enforce one.")
    else:
        print("\n  WARNING: Both are DISABLED. Run 'ai-switch.py copilot' or 'ai-switch.py amazonq' to restore one.")


def switch(target: str):
    current = read_state()

    if target == current:
        print(f"[INFO] {target.capitalize()} is already the active assistant.")
        get_status()
        return

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] VS Code database not found: {DB_PATH}")
        sys.exit(1)

    # Backup before modification
    backup = DB_PATH + ".ai-switch.bak"
    shutil.copy2(DB_PATH, backup)

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cur = conn.cursor()

        disabled = read_enablement(cur)
        # Start from scratch: remove all known IDs, then disable the inactive set
        all_known = set(COPILOT_IDS + AMAZONQ_IDS)
        disabled = [d for d in disabled if d not in all_known]

        if target == "copilot":
            disabled.extend(AMAZONQ_IDS)
        elif target == "amazonq":
            disabled.extend(COPILOT_IDS)

        write_enablement(cur, disabled)
        conn.commit()
        conn.close()

    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower() or "busy" in str(e).lower():
            print(
                "[ERROR] Database is locked.\n"
                "Use Ctrl+Shift+P > Reload Window in VS Code first, then retry."
            )
        else:
            print(f"[ERROR] SQLite error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    write_state(target)

    if target == "copilot":
        print(BANNER_COPILOT)
    else:
        print(BANNER_AMAZONQ)


def main():
    parser = argparse.ArgumentParser(
        description="Switch between GitHub Copilot Chat and Amazon Q in VS Code."
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["copilot", "amazonq", "status"],
        default="status",
        help="Which assistant to activate, or 'status' to check current state"
    )
    args = parser.parse_args()

    if args.action == "status":
        get_status()
    else:
        switch(args.action)


if __name__ == "__main__":
    main()
