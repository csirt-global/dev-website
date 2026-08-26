#!/usr/bin/env python3
"""Fail before /.well-known/security.txt expires, not after.

RFC 9116 makes `Expires` mandatory and says a file past that date must not be
relied on. The previous one lapsed on 2025-01-01 and stayed published, which is
issue #56 — nothing was watching it, so nobody knew.

Thirty days of warning is enough to open a pull request and not enough to
forget about.
"""
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "static" / ".well-known" / "security.txt"
GRACE = timedelta(days=30)


def main() -> int:
    if not FILE.exists():
        print(f"::error::{FILE} is missing")
        return 1

    text = FILE.read_text()
    m = re.search(r"^Expires:\s*(\S+)\s*$", text, re.M)
    if not m:
        print("::error::security.txt has no Expires field (RFC 9116 requires one)")
        return 1

    raw = m.group(1).replace("Z", "+00:00")
    try:
        expires = datetime.fromisoformat(raw)
    except ValueError:
        print(f"::error::security.txt Expires is not a valid timestamp: {m.group(1)}")
        return 1

    now = datetime.now(timezone.utc)
    left = expires - now
    print(f"security.txt expires : {expires.date()} ({left.days} days)")

    if left <= timedelta(0):
        print("::error::security.txt has expired - RFC 9116 says it must not be relied on")
        print("\nFAIL: security.txt has expired")
        return 1
    if left <= GRACE:
        print(f"::error::security.txt expires in {left.days} days - renew the Expires field")
        print("\nFAIL: security.txt is about to expire")
        return 1

    # Contact is the other mandatory field.
    if not re.search(r"^Contact:\s*\S+", text, re.M):
        print("::error::security.txt has no Contact field (RFC 9116 requires one)")
        print("\nFAIL: security.txt is incomplete")
        return 1

    print("\nPASS: security.txt is valid and not close to expiring")
    return 0


if __name__ == "__main__":
    sys.exit(main())
