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

Thresholds live in LANGUAGES below, one per language. A language at 1.00 is
finished and enforced: adding an English page without it fails the build. A
language still being written sits at 0.00 and is only reported. Raise it when the
language is complete.

Two things are counted but never block. `unreviewed` is how many translated
pages no native speaker has signed off, which will never be zero in a volunteer
organisation. `english` is how many translated files still read as English, and
that one does block, because it is a defect rather than a missing signature.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DEFAULT_LANG = "en"

# lang: minimum fraction of pages that must be translated for the build to pass
# A threshold is per language and says one thing: this language is complete, keep
# it that way. A language still being filled in sits at 0.00 and is only reported,
# which is how English, then Dutch, German, French and Spanish each got here.
#
# So a new language starts at 0.00, gets written, and is raised when it is done.
# Raising it is the last step of adding a language, not a precondition.
LANGUAGES = {
    "en": 1.00,
    "nl": 1.00,
    "de": 1.00,
    "fr": 1.00,
    "es": 1.00,
    "pt-br": 0.00,   # being written
    "zh": 0.00,      # being written
}


# A body this similar to its English source has not been translated, whatever
# the front matter claims. Tuned so a genuine translation of a short page full
# of identifiers still passes: CG-2024-00001's Dutch body shares proper nouns,
# CVEs and version strings with the English and lands well under this.
ENGLISH_OVERLAP = 0.85


def body_tokens(path: Path) -> set:
    """Words of the body, without front matter, markup or identifiers.

    Identifiers are stripped because they are supposed to be identical in every
    language. Leaving them in would make a properly translated case page look
    like an untranslated one.
    """
    text = path.read_text()
    body = text.split("---", 2)[-1]
    body = re.sub(r"\{\{<[^>]*>\}\}", " ", body)          # shortcodes
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)     # link targets
    body = re.sub(r"`[^`]*`", " ", body)                   # code spans
    body = re.sub(r"https?://\S+", " ", body)               # bare URLs
    words = re.split(r"[^0-9A-Za-z\u00c0-\u024f]+", body.lower())
    return {w for w in words
            if len(w) > 3 and not re.fullmatch(r"(cve|cwe|cpe|cg)?[0-9].*", w)}


def is_reviewed(path: Path) -> bool:
    """True when a native speaker has signed the page off in its front matter."""
    return bool(re.search(r"^reviewed:\s*true\s*$", path.read_text(), re.M))


def looks_like_source(translated: Path, source: Path) -> float:
    """Fraction of the translation's words that also appear in the English."""
    t, s = body_tokens(translated), body_tokens(source)
    if len(t) < 12:            # too short to judge; the title carries it
        return 0.0
    return len(t & s) / len(t)


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
    print(f"{'language':<10} {'translated':>12} {'missing':>9} {'stale':>7} {'english':>8} {'unreviewed':>11}   status")
    print("-" * 86)

    details: list[str] = []
    for lang, threshold in LANGUAGES.items():
        translated = missing = stale = english = unreviewed = 0
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
                if lang != DEFAULT_LANG and src:
                    if git_mtime(src) > git_mtime(byline[lang]):
                        stale += 1
                        details.append(f"  stale   [{lang}] {key}")
                    # The flag above is manual, so it only catches the honest
                    # mistake. This catches the other one.
                    overlap = looks_like_source(byline[lang], src)
                    if overlap >= ENGLISH_OVERLAP:
                        english += 1
                        details.append(
                            f"  ENGLISH [{lang}] {key} "
                            f"({overlap:.0%} of its words are in the English body)"
                        )
                    if not is_reviewed(byline[lang]):
                        unreviewed += 1
            else:
                missing += 1
                details.append(f"  missing [{lang}] {key}")

        coverage = translated / total
        ok = coverage >= threshold and not (threshold >= 1.0 and stale) and not english
        if not ok:
            failed = True
        print(
            f"{lang:<10} {translated:>4}/{total:<3} {coverage:>5.0%} "
            f"{missing:>9} {stale:>7} {english:>8} {unreviewed:>11}   "
            f"{'ok' if ok else 'FAIL'} (need {threshold:.0%})"
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
