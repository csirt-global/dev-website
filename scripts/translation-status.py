#!/usr/bin/env python3
"""Report which pages are translated, missing, or stale, per language.

Why this exists
---------------
A five-language site fails quietly. Hugo falls back to the default language
when a translation is absent, so a page that was never translated looks fine
to anyone who does not read that language. DIVD's site shows where that ends
up: full i18n machinery, `.en.md` on all 66 content files, a language switcher
rendered twice, `locales: [en, nl]` in two CMS configs, and zero translated
pages.

This makes the gap countable. Run it locally or in CI.

Stale means the source-language file was modified more recently than the
translation, so the translation is probably behind. That is a heuristic on
git mtimes, not a semantic diff, but it catches the common case: someone edits
the English page and forgets the other four.

Exit codes
----------
0  every language meets its required coverage
1  a language below its threshold, or a missing/stale page in a strict language

Thresholds live in LANGUAGES below. Only English is strict for now: the decision is to stabilise the English
site first and translate afterwards. Every other language is tracked and
listed on each run, so the gap stays visible, so the
build stays green while translations are still being produced. Tighten a
threshold the moment a language has a committed reviewer.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DEFAULT_LANG = "en"

# lang: minimum fraction of pages that must be translated for the build to pass
LANGUAGES = {
    "en": 1.00,
    "nl": 0.00,   # English-first: stabilise EN, then translate
    "de": 0.00,
    "fr": 0.00,
    "es": 0.00,
}


def git_mtime(path: Path) -> int:
    """Last commit time for a file, falling back to filesystem mtime."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if out:
            return int(out)
    except Exception:
        pass
    return int(path.stat().st_mtime)


def page_key(path: Path) -> str:
    """Identify a page independent of its language suffix.

    content/_index.en.md            -> _index
    content/cases/foo/index.nl.md   -> cases/foo/index
    """
    rel = path.relative_to(CONTENT)
    stem = rel.name
    for lang in LANGUAGES:
        if stem.endswith(f".{lang}.md"):
            stem = stem[: -len(f".{lang}.md")]
            break
    return str(rel.parent / stem) if str(rel.parent) != "." else stem


def main() -> int:
    pages: dict[str, dict[str, Path]] = {}
    for md in sorted(CONTENT.rglob("*.md")):
        lang = next((l for l in LANGUAGES if md.name.endswith(f".{l}.md")), None)
        if lang is None:
            print(f"  ! {md.relative_to(ROOT)} has no language suffix, skipping")
            continue
        pages.setdefault(page_key(md), {})[lang] = md

    total = len(pages)
    if total == 0:
        print("no content pages found")
        return 1

    failed = False
    print(f"{'language':<10} {'translated':>12} {'missing':>9} {'stale':>7}   status")
    print("-" * 62)

    details: list[str] = []
    for lang, threshold in LANGUAGES.items():
        translated = missing = stale = 0
        for key, byline in sorted(pages.items()):
            f = byline.get(lang)
            # A file that exists but is explicitly flagged as still carrying the
            # source language does not count. Copying English into a .nl.md and
            # calling it translated is exactly the drift this script exists to
            # catch.
            if f is not None and "untranslated: true" in f.read_text():
                missing += 1
                details.append(f"  untranslated [{lang}] {key} (file exists, body not translated)")
                continue
            if lang in byline:
                translated += 1
                src = byline.get(DEFAULT_LANG)
                if lang != DEFAULT_LANG and src and git_mtime(src) > git_mtime(byline[lang]):
                    stale += 1
                    details.append(f"  stale   [{lang}] {key}")
            else:
                missing += 1
                details.append(f"  missing [{lang}] {key}")

        coverage = translated / total
        ok = coverage >= threshold and not (threshold >= 1.0 and stale)
        if not ok:
            failed = True
        print(
            f"{lang:<10} {translated:>4}/{total:<3} {coverage:>5.0%} "
            f"{missing:>9} {stale:>7}   "
            f"{'ok' if ok else 'BELOW THRESHOLD'} (need {threshold:.0%})"
        )

    if details:
        print()
        for line in details:
            print(line)

    print()
    print("FAIL: a language is below its required coverage" if failed
          else "PASS: all languages meet their required coverage")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
