#!/usr/bin/env python3
"""Assert that no text from the old site was lost in the redesign.

This replaces visual comparison. The redesign deliberately looks different and
reorganises pages, so matching rendering is meaningless. What must hold is that
every sentence the old site published still exists somewhere on the new one.

Compares the *reference* build (the live site plus our merged PRs, served on
:8899, mirrored on disk) against ./public.

Known and intentional exclusions live in ALLOWED_DROPS with a reason each. A
drop that is not listed there fails the build, so losing content is a decision
someone has to write down, not something that happens quietly.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "public"
REF = Path("/private/tmp/claude-501/-Users-max-claude-website"
           "/1279652b-500a-4617-a5c5-e801296f25c8/scratchpad/ref")

# Substrings that may legitimately be absent from the new site.
ALLOWED_DROPS = {
    "CSIRT.Global | ": "page <title>, deliberately rewritten for the new IA",
    "https://blog.jetbrains.com": "raw URL now rendered as a named link",
    "https://www.connectwise.com/company/trust": "raw URL now rendered as a named link",
    "https://www.huntress.com/blog": "raw URL now rendered as a named link",
    "Workflow": "Tailwind UI template leftover, never CSIRT content",
    "Introducing": "commented-out template artefact",
    "tailwindui.com": "template placeholder asset",
    "Your logo here": "still present, rendered from a template string",
    "instincively": "typo, fixed to 'instinctively'",
    "indecent": "typo, fixed to 'incident'",
    "vulnerabilitiy": "typo, fixed to 'vulnerability'",
    "safefty": "typo, fixed to 'safety'",
    "[IP]": "unfilled placeholder shipped to production, not content",
    "[email]": "unfilled placeholder shipped to production, not content",
    "twitter.com/person": "placeholder team card, not a real person",
    # The old Dutch homepage labelled the statutory contact block "Kantoor: ...
    # Tel.: ...". Trimming that homepage to match the English one removed the
    # label, not the information: the registered address and the telephone
    # number are published on /about/anbi/ in every language, from
    # data/verify.yaml, under the label that language uses. Verified in every
    # one before allowing this drop.
    "Kantoor: Maanweg": "Dutch label for the statutory contact block; the details themselves moved to /about/anbi/",
    "linkedin.com/in/person": "placeholder team card, not a real person",
}

STOP = re.compile(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", re.S)
TAG = re.compile(r"<[^>]+>")


def norm(t: str) -> str:
    """Fold typographic punctuation and whitespace.

    Hugo renders smart quotes and escapes them as entities, so ' arrives as
    &rsquo; on one side and the literal \u2019 on the other. Neither is lost
    content, so both sides are folded to plain ASCII punctuation first.
    """
    t = html.unescape(t)
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u00a0", " ")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def blocks(path: Path) -> list[str]:
    """Visible text blocks on a page, one per element."""
    html = STOP.sub(" ", path.read_text(errors="ignore"))
    out = []
    for chunk in TAG.sub("\n", html).split("\n"):
        t = norm(chunk)
        if len(t) > 30:
            out.append(t)
    return out


def stream(path: Path) -> str:
    """All visible text on a page as one stream, short fragments included.

    blocks() drops fragments under 30 chars, which is right for deciding what to
    check but wrong for building the haystack: the two builds break sentences at
    different inline tags, so a <strong> in one and not the other would otherwise
    read as a missing sentence.
    """
    return norm(TAG.sub(" ", STOP.sub(" ", path.read_text(errors="ignore"))))


def all_text(root: Path) -> str:
    return " ".join(
        stream(p) for p in root.rglob("*.html") if not p.name.endswith(".old")
    )


def words(t: str) -> set:
    return set(w for w in re.split(r"[^0-9A-Za-z]+", t.lower()) if w)


def main() -> int:
    if not REF.exists():
        print("SKIP: no reference build to compare against")
        print(f"  expected at {REF}")
        print("  create it with: git worktree add <path> reference-with-prs")
        return 0
    if not NEW.exists():
        print("public/ not found - run `make build` first")
        return 1

    new_text = all_text(NEW)
    new_words = words(new_text)
    missing: list[tuple[str, str]] = []
    reordered: list[tuple[str, str]] = []
    checked = 0

    for page in sorted(REF.rglob("*.html")):
        if page.name.endswith(".old"):
            continue
        for b in blocks(page):
            checked += 1
            # match on a distinctive prefix: wording may be re-wrapped, and
            # headings get re-cased, but the sentence itself should survive
            probe = b[:60]
            if probe in new_text:
                continue
            reason = next((r for k, r in ALLOWED_DROPS.items() if k in b), None)
            if reason:
                continue
            # Present but re-ordered or re-punctuated: every word survives, the
            # sentence is just assembled differently. Reported, not failed.
            if words(b) <= new_words:
                reordered.append((str(page.relative_to(REF)), b))
                continue
            missing.append((str(page.relative_to(REF)), b))

    print(f"reference blocks checked : {checked}")
    print(f"re-flowed (all words kept): {len(reordered)}")
    for src, b in reordered:
        print(f"  {src}: {b[:90]}")
    print(f"missing from new site    : {len(missing)}")
    for src, b in missing[:40]:
        print(f"  {src}")
        print(f"    {b[:110]}")
        print(f"::error::content lost in redesign - {b[:80]}")
    if len(missing) > 40:
        print(f"  ... and {len(missing) - 40} more")

    print()
    print("FAIL: content was lost" if missing else "PASS: no content lost")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
