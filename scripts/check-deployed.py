#!/usr/bin/env python3
"""Check the site that was actually published, not the folder it was built from.

Every other check in this repository reads ./public. That is the folder Hugo
wrote, and it is not the same thing as what visitors get: between the two sits
the artifact upload, which can drop files.

It already nearly happened. actions/upload-pages-artifact v4 stopped including
hidden files, which would have removed /.well-known/security.txt from the
published site. check-urls.py would still have passed, because the file was
there in ./public, and the deploy would still have reported success. Only the
live URL would have been wrong.

So this runs after deployment and fetches real URLs over the network. The list
is imported from check-urls.py rather than repeated, so the build and the
published site are held to the same one.

Usage:  python3 scripts/check-deployed.py https://staging.csirt.global/
"""
import importlib.util
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIMEOUT = 20
ATTEMPTS = 3


def _load_urls():
    """Import the required-URL lists from check-urls.py (hyphen, so by path)."""
    spec = importlib.util.spec_from_file_location("check_urls", ROOT / "check-urls.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ANBI, mod.PAGES


def fetch(url: str):
    """Return (status, body). Retries: Pages can lag a moment behind a deploy."""
    last = None
    for attempt in range(ATTEMPTS):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "csirt-global-deploy-check"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, r.read(4096).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = (e.code, "")
        except Exception as e:                       # network hiccup, DNS, TLS
            last = (0, str(e))
        if attempt < ATTEMPTS - 1:
            time.sleep(3 * (attempt + 1))
    return last


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    base = sys.argv[1].rstrip("/")
    anbi, pages = _load_urls()
    failed = []

    def check(path: str, must_contain: str = "") -> None:
        url = base + urllib.parse.quote(path, safe="/:%")
        status, body = fetch(url)
        ok = status == 200 and (not must_contain or must_contain in body)
        note = "" if status == 200 else f" (HTTP {status})"
        if not ok and status == 200:
            note = f" (200 but missing {must_contain!r})"
        print(f"  {'ok  ' if ok else 'FAIL'} {path}{note}")
        if not ok:
            failed.append(path)
            print(f"::error::published site: {path} is not being served correctly{note}")

    print(f"Checking the published site at {base}/\n")

    print("Statutory ANBI documents")
    for u in anbi:
        check(u)

    print("\nCitable pages")
    for u in pages:
        check(u)

    print("\nFiles that live in a hidden directory")
    # The case that started this. security.txt sits inside /.well-known/, which
    # is hidden, so an artifact that skips hidden files silently drops it.
    check("/.well-known/security.txt", must_contain="Contact:")

    print("\nCase URLs are case-sensitive")
    lower = "/cases/cg-2024-00001/"
    status, _ = fetch(base + lower)
    ok = status != 200
    print(f"  {'ok  ' if ok else 'FAIL'} {lower} does not resolve (HTTP {status})")
    if not ok:
        failed.append(lower)
        print("::error::published site: lowercased case URLs resolve, so the capitals are not being preserved")

    print()
    print(f"FAIL: {len(failed)} published URL(s) wrong" if failed else "PASS: the published site serves everything it must")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
