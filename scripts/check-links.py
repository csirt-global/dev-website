#!/usr/bin/env python3
"""Check that internal links and assets in the built site actually resolve.

The old site shipped a link with no scheme (href="csirt.divd.nl/...") that
resolved under /projects/pgngo/ and 404'd, a mobile-menu logo pointing at a
Tailwind UI asset that no longer exists, and a Markdown file at /anbi/ that
GitHub Pages never rendered. All three were live for months. This catches that
class of problem before merge.

External links are reported but not fetched: a third-party outage should not
fail our build.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

ATTR = re.compile(r'(?:href|src)=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))')


STRAY = re.compile(r"[(\[]\s+<a\s|</a>\s+[.,;:)\]!?]")


def stray_space(root: Path) -> list[tuple[str, str]]:
    """Links with whitespace welded to the punctuation around them.

    A render hook emits its template's whitespace verbatim, so one untrimmed
    newline becomes a space in every sentence containing a link: "( DIVD)",
    "case register , with the date". Invisible in the template, obvious on
    the page.
    """
    out = []
    for p in sorted(root.rglob("*.html")):
        for m in STRAY.finditer(p.read_text(errors="ignore")):
            out.append((str(p.relative_to(root)), m.group(0).replace("\n", "\\n")))
    return out


def main() -> int:
    if not PUBLIC.exists():
        print("public/ not found - run `make build` first")
        return 1

    broken: list[str] = []
    external = 0
    checked = 0

    for page in sorted(PUBLIC.rglob("*.html")):
        html = page.read_text(errors="ignore")
        rel_page = page.relative_to(PUBLIC)
        for m in ATTR.finditer(html):
            raw = m.group(1) or m.group(2) or m.group(3) or ""
            # /livereload.js is injected by `hugo server`, never by a real build
            if raw.startswith("/livereload.js"):
                continue
            if not raw or raw.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
                continue
            parsed = urlparse(raw)
            if parsed.scheme in ("http", "https") or raw.startswith("//"):
                external += 1
                continue

            checked += 1
            target = unquote(parsed.path.split("#")[0])
            if not target:
                continue
            if target.startswith("/"):
                dest = PUBLIC / target.lstrip("/")
            else:
                dest = page.parent / target
            if dest.is_dir():
                dest = dest / "index.html"
            if not dest.exists():
                broken.append(f"{rel_page}: {raw}")

    print(f"pages scanned   : {len(list(PUBLIC.rglob('*.html')))}")
    print(f"internal links  : {checked}")
    print(f"external links  : {external} (not fetched)")
    print(f"broken          : {len(broken)}")
    for b in broken:
        print(f"  {b}")
        print(f"::error::broken internal link - {b}")

    stray = stray_space(PUBLIC)
    print(f"stray space at links: {len(stray)}")
    for src, frag in stray[:10]:
        print(f"  {src}: {frag!r}")
        print(f"::error::stray whitespace around a link - {src}")

    print()
    ok = not broken and not stray
    print("PASS: all internal links resolve" if ok else "FAIL: link problems")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
