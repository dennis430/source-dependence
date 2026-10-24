#!/usr/bin/env python3
"""Deterministic daily status controller. Persists state. No model calls."""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

STATE_PATH = Path("state/daily_state.json")
LEDGER_PATH = Path("state/decision_ledger.jsonl")

def main():
    now = datetime.now(timezone.utc).isoformat()
    state = {"last_check": now, "status": "LIVE_TRIAL", "notes": []}
    try:
        py = Path("pyproject.toml").read_bytes()
        state["pyproject_sha256"] = hashlib.sha256(py).hexdigest()[:16]
    except Exception as e:
        state["notes"].append(f"integrity_check_error: {e}")
    STATE_PATH.parent.mkdir(exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))
    with LEDGER_PATH.open("a") as f:
        f.write(json.dumps({"ts": now, "action": "daily_status", "state_summary": state["status"]}) + "\n")
    print(json.dumps({"ok": True, "state_written": str(STATE_PATH), "ts": now}))

if __name__ == "__main__":
    main()
