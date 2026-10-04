#!/usr/bin/env python3
"""Verify that every URL the old site served still resolves in the new build.

Victor named the ANBI contact details and their documents as the key
requirement for the rebuild, because the Dutch tax authority (Belastingdienst)
relies on them being published. Those are legal obligations, so they are
checked separately and loudly.

The case pages are externally citable and their URLs are case-sensitive on
GitHub Pages, so /cases/CG-2024-00001/ must not become /cases/cg-2024-00001/.

Run against the built ./public directory.
"""
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# Legal obligation: must never 404.
ANBI = [
    "/uploads/CSIRT financieel verslag 2022.pdf",
    "/uploads/CSIRT financieel verslag 2023.pdf",
    "/uploads/CSIRT financieel verslag 2024.pdf",
    "/uploads/CSIRT.global annual overview 2022.pdf",
    "/uploads/extract_trade register_CSIRT.global.pdf",
    "/uploads/standaardform-pubplicht-anbi-algemeen-2024.pdf",
    "/uploads/Standard form for publication obligation Fundraising organisations including financials 2022.pdf",
]

# Externally citable, case-sensitive.
PAGES = [
    "/",
    "/notified/",
    "/what-we-do/",
    "/what-we-do/bug-bounties/",
    "/what-we-do/exploit-research/",
    "/what-we-do/incident-response/",
    "/cases/",
    "/cases/CG-2024-00001/",
    "/cases/CG-2024-00002/",
    "/cases/CG-2024-00003/",
    "/projects/",
    "/projects/pgu/",
    "/projects/pgngo/",
    "/about/",
    "/about/team/",
    "/about/code-of-conduct/",
    "/about/anbi/",
    "/get-involved/",
    "/news/",
    "/join/",
    "/code/",
    "/.well-known/security.txt",
    "/llms.txt",
]

# Fragment anchors other pages and external links target. Checked as substrings
# of the rendered homepage rather than as separate URLs.
# The old site was one page with anchors. They are linked externally, so the
# homepage must still carry a mapping for them.
LEGACY_ANCHORS = ["#mission", "#news", "#organisation", "#team", "#board",
                  "#code", "#help", "#anbi", "#documents", "#soufian", "#lennaert"]


def exists(url: str) -> bool:
    rel = unquote(url).lstrip("/")
    target = PUBLIC / rel
    if url.endswith("/") or target.is_dir():
        target = PUBLIC / rel / "index.html"
    return target.exists()


def main() -> int:
    if not PUBLIC.exists():
        print("public/ not found — run `make build` first")
        return 1

    failed = False

    print("ANBI documents (Belastingdienst requirement)")
    for u in ANBI:
        ok = exists(u)
        failed |= not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {u}")

    print("\nCitable pages")
    for u in PAGES:
        ok = exists(u)
        failed |= not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {u}")

    home = (PUBLIC / "index.html").read_text() if (PUBLIC / "index.html").exists() else ""
    print("\nLegacy anchors still handled")
    for a in LEGACY_ANCHORS:
        ok = f'"{a}"' in home
        failed |= not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {a}")

    # Case-sensitivity guard: catch a lowercased case directory explicitly,
    # since it would 404 on Pages while looking fine on a Mac's case-insensitive
    # filesystem.
    print("\nURL case preservation")
    lower = PUBLIC / "cases" / "cg-2024-00001"
    upper = PUBLIC / "cases" / "CG-2024-00001"
    actual = [p.name for p in (PUBLIC / "cases").iterdir() if p.is_dir()] if (PUBLIC / "cases").exists() else []
    ok = "CG-2024-00001" in actual
    failed |= not ok
    print(f"  {'ok  ' if ok else 'FAIL'} /cases/CG-2024-00001/ (found: {', '.join(actual) or 'nothing'})")

    print()
    print("FAIL: at least one required URL is missing" if failed else "PASS: all required URLs resolve")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
