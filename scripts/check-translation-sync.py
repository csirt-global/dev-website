#!/usr/bin/env python3
"""Assert that a change to one language is made in all of them.

The rule: if a pull request edits a page in one language, it edits that page in
every language it exists in. A correction to a case record is a correction in
seven files, or the site drifts back to a few accurate versions and several that
quietly disagree.

This reads the *diff*, not the state of the repository, and that distinction is
the design. Comparing file timestamps looked simpler and does not work: every
language here was written in its own pull request, so each language's files were
committed days apart by construction. Timestamps say Spanish is the newest
version of every page on the site, which is true and means nothing.

Adding a translation is not editing one. A new file is how a language gets
written in the first place, so only modifications and deletions oblige the rest
to follow.

When a change genuinely does not apply to the other languages, say so in the
commit message rather than making six no-op edits:

    Translation-sync: not-required, fixes a Dutch-only typo

Usage:  python3 scripts/check-translation-sync.py [base-ref]
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERRIDE = re.compile(r"^Translation-sync:\s*not-required\b", re.M | re.I)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()


def languages() -> list[str]:
    """The configured languages, read from hugo.yaml rather than repeated here."""
    out, inside = [], False
    for line in (ROOT / "hugo.yaml").read_text().splitlines():
        if line.startswith("languages:"):
            inside = True
            continue
        if inside:
            if line and not line.startswith(" "):
                break
            m = re.match(r"^  ([A-Za-z][\w-]*):\s*$", line)
            if m:
                out.append(m.group(1))
    return out


def page_of(path: str, langs: list[str]) -> tuple[str, str] | None:
    """content/a/b/index.pt-br.md -> ("content/a/b/index", "pt-br")."""
    for lang in sorted(langs, key=len, reverse=True):
        if path.endswith(f".{lang}.md"):
            return path[: -len(f".{lang}.md")], lang
    return None


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    langs = languages()
    if not langs:
        print("::error::could not read any languages from hugo.yaml")
        return 1

    diff = git("diff", "--name-status", f"{base}...HEAD", "--", "content/")
    if not diff:
        print(f"no content changed against {base}")
        print("\nPASS: nothing to keep in sync")
        return 0

    touched: dict[str, dict[str, str]] = {}
    for line in diff.splitlines():
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        split = page_of(path, langs)
        if split:
            touched.setdefault(split[0], {})[split[1]] = status[0]

    print(f"languages configured : {', '.join(langs)}")
    print(f"pages touched        : {len(touched)}")

    behind: list[str] = []
    for page, by_lang in sorted(touched.items()):
        edited = {l for l, st in by_lang.items() if st in ("M", "D")}
        if not edited:
            continue
        exists = {l for l in langs if (ROOT / f"{page}.{l}.md").exists()}
        missing = sorted(exists - set(by_lang))
        if missing:
            behind.append(f"{page}: edited in {', '.join(sorted(edited))}, "
                          f"untouched in {', '.join(missing)}")

    if behind and OVERRIDE.search(git("log", f"{base}..HEAD", "--format=%B")):
        print("\noverridden by a Translation-sync trailer in the commit message:")
        for b in behind:
            print(f"  allowed {b}")
        print("\nPASS: out of sync, and the reason is written down")
        return 0

    for b in behind:
        print(f"  FAIL {b}")
        print(f"::error::translation out of sync - {b}")

    print()
    print("FAIL: a page was edited in some languages and not others" if behind
          else "PASS: every edited page was edited in every language it has")
    return 1 if behind else 0


if __name__ == "__main__":
    sys.exit(main())
