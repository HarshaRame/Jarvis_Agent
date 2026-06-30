"""
Clear VS Code Copilot chat sessions older than N days (default: 4).

Usage:
    python clear-old-chats.py [--days 4] [--dry-run]

NOTE: Close VS Code before running this script to avoid database lock conflicts.
      This script is OS-agnostic and works on Windows, macOS, and Linux.
"""

import sqlite3
import json
import shutil
import os
import sys
import time
import argparse
import platform
from datetime import datetime, timezone

# Determine OS-specific database path
if platform.system() == "Windows":
    DB_PATH = os.path.join(
        os.environ.get("APPDATA", os.path.expanduser("~")),
        "Code", "User", "globalStorage", "state.vscdb"
    )
else:  # macOS and Linux
    DB_PATH = os.path.expanduser(
        "~/.config/Code/User/globalStorage/state.vscdb"
    )
CHAT_INDEX_KEY = "chat.ChatSessionStore.index"


def ms_to_datetime(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone()


def clear_old_chats(days: int = 4, dry_run: bool = False) -> None:
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found: {DB_PATH}")
        sys.exit(1)

    cutoff_ms = int(time.time() * 1000) - (days * 24 * 60 * 60 * 1000)
    cutoff_dt = ms_to_datetime(cutoff_ms)
    print(f"Cutoff: sessions with last activity before {cutoff_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    if dry_run:
        print("[DRY RUN] No changes will be made.\n")

    # Back up the database before any modification
    backup_path = DB_PATH + ".bak"
    if not dry_run:
        shutil.copy2(DB_PATH, backup_path)
        print(f"Backup created: {backup_path}")

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cur = conn.cursor()

        cur.execute("SELECT value FROM ItemTable WHERE key = ?", (CHAT_INDEX_KEY,))
        row = cur.fetchone()

        if not row or not row[0]:
            print("No chat session index found. Nothing to clear.")
            conn.close()
            return

        index = json.loads(row[0])
        entries = index.get("entries", {})
        total = len(entries)

        to_remove = []
        for session_id, entry in entries.items():
            last_activity = entry.get("lastMessageDate") or entry.get("timing", {}).get("created", 0)
            if last_activity < cutoff_ms:
                to_remove.append((session_id, entry.get("title", "Untitled"), last_activity))

        if not to_remove:
            print(f"No sessions older than {days} days found (total sessions: {total}).")
            conn.close()
            return

        print(f"\nFound {len(to_remove)} session(s) to remove (out of {total}):")
        for sid, title, ts in to_remove:
            age_days = (int(time.time() * 1000) - ts) / (1000 * 86400)
            print(f"  [{age_days:.1f}d] {title!r}  (id: {sid[:8]}...)")

        if dry_run:
            print("\n[DRY RUN] Would remove the above sessions.")
            conn.close()
            return

        # Remove old sessions from the index
        for sid, _, _ in to_remove:
            del entries[sid]

        index["entries"] = entries
        updated_value = json.dumps(index, separators=(",", ":"))

        cur.execute(
            "UPDATE ItemTable SET value = ? WHERE key = ?",
            (updated_value, CHAT_INDEX_KEY)
        )
        conn.commit()
        conn.close()

        print(f"\nRemoved {len(to_remove)} session(s). Remaining: {len(entries)}.")

    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower() or "busy" in str(e).lower():
            print(
                f"\n[ERROR] Database is locked — VS Code is likely running.\n"
                f"Close VS Code and re-run this script.\n"
                f"Details: {e}"
            )
        else:
            print(f"\n[ERROR] SQLite error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Clear VS Code Copilot chat sessions older than N days."
    )
    parser.add_argument(
        "--days", type=int, default=4,
        help="Remove sessions with no activity for more than this many days (default: 4)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview what would be removed without making changes"
    )
    args = parser.parse_args()

    clear_old_chats(days=args.days, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
