#!/usr/bin/env python3
"""Assert that every component class a layout uses actually exists in the CSS.

The previous site shipped 17 utility classes that were used on live pages and
present in no stylesheet, because the compiled CSS was committed and went 2.5
years without a rebuild. Nothing checked, so nobody noticed.

This repo rebuilds the CSS every time, which fixes that — but not the other
direction. Component classes (.record, .status, .btn, .verify …) are hand-written
in main.css, so deleting one while editing leaves every template that uses it
silently unstyled. That happened here: a careless splice removed the whole case
record block, and the case register rendered as plain text for three commits
before anyone looked at it.

Tailwind utilities are not checked: they are generated from the same templates
this reads, so they cannot go missing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets" / "css" / "main.css"
LAYOUTS = ROOT / "layouts"

# Prefixes of the hand-written component layer. A class matching one of these
# must have a rule; anything else is a Tailwind utility and is generated.
COMPONENT = re.compile(r"^(t-|prose-|on-paper|verify|btn|nav-link|nav-drop|record|status|notice|hero-mark|support|staging-)[\w-]*$")


def main() -> int:
    css = CSS.read_text()
    used: dict[str, set] = {}
    for page in sorted(LAYOUTS.rglob("*.html")):
        for m in re.finditer(r'class="([^"]*)"', page.read_text()):
            for c in m.group(1).split():
                if COMPONENT.match(c):
                    used.setdefault(c, set()).add(str(page.relative_to(ROOT)))

    missing = {c: v for c, v in used.items() if f".{c}" not in css}
    print(f"component classes used : {len(used)}")
    print(f"missing a rule         : {len(missing)}")
    for c, where in sorted(missing.items()):
        print(f"  .{c} - used in {', '.join(sorted(where))}")
        print(f"::error::component class .{c} has no rule in assets/css/main.css")

    print()
    print("FAIL: a layout uses a component class that does not exist"
          if missing else "PASS: every component class has a rule")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
