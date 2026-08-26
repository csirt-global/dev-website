#!/usr/bin/env python3
"""Assert that the donate page and its settings agree with each other.

Issue #18 asked for a donate button. Everything is built except the provider and
the URL, which nobody could supply, so the page ships switched off. Two things
have to move together to switch it on: `enabled` in data/donate.yaml, and the
`hidden`/`noindex` flags on the page itself. Doing one without the other gives
you either a live page nobody can reach, or a reachable page with buttons that
go nowhere — on a page that asks people for money.

So this check enforces both directions, and refuses a half-configured live page.

No YAML dependency: the file is flat by design and this reads only the handful
of scalars it needs, so the check runs anywhere python3 does.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "donate.yaml"
PAGE = ROOT / "content" / "get-involved" / "donate" / "index.en.md"
BUILT = ROOT / "public" / "get-involved" / "donate" / "index.html"
ALIAS = ROOT / "public" / "donate" / "index.html"
HOME = ROOT / "public" / "index.html"


def linkers() -> list[str]:
    """Pages that link to the donate page, excluding it and its own alias."""
    out = []
    for p in (ROOT / "public").rglob("*.html"):
        rel = str(p.relative_to(ROOT / "public"))
        if rel.startswith(("donate/", "get-involved/donate/")):
            continue
        if "get-involved/donate" in p.read_text(errors="ignore"):
            out.append(rel)
    return sorted(out)


def settings(path: Path) -> dict:
    """Flat read of the keys this check needs: `key` and `parent.key`."""
    out, parent = {}, ""
    for raw in path.read_text().splitlines():
        line = raw.split("#")[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w]*):\s*(.*)$", line)
        if not m:
            continue
        indent, key, val = len(m.group(1)), m.group(2), m.group(3).strip()
        if indent == 0:
            parent = ""
            if val == "":
                parent = key
                continue
        name = f"{parent}.{key}" if indent and parent else key
        out[name] = val.strip('"').strip("'")
    return out


def main() -> int:
    if not BUILT.exists():
        print("public/ not found - run `make build` first")
        return 1

    s = settings(DATA)
    enabled = s.get("enabled", "false").lower() == "true"
    # Read the front matter as lines, ignoring comments: the page's own comment
    # explains how to restore `hidden: true`, and a substring match found that
    # and reported the flag as set.
    front = [l for l in PAGE.read_text().split("---")[1].splitlines()
             if not l.lstrip().startswith("#")]
    flag = lambda k: any(re.match(rf"^{k}:\s*true\s*$", l) for l in front)
    hidden, noindex = flag("hidden"), flag("noindex")
    html = BUILT.read_text()
    bad = []

    print(f"donate.enabled       : {enabled}")
    print(f"page hidden/noindex  : {hidden}/{noindex}")

    sample = s.get("sample", "false").lower() == "true"
    if enabled and sample:
        # Reviewable on a staging copy, never on the live site. robots.txt is
        # generated from the baseURL, so the build itself says which this is.
        robots = ROOT / "public" / "robots.txt"
        production = robots.exists() and "Allow: /" in robots.read_text()
        msg = "donate is switched on with SAMPLE data - every payment route is a placeholder"
        # What must never happen is sample payment routes reaching the live
        # site, and only a deploy can do that. A local build and a pull request
        # both build against hugo.yaml's default baseURL, which is the live
        # host, but neither publishes anything. So the refusal is deploy plus
        # the live host; everything else warns. deploy.yml sets DEPLOYING.
        if production and os.environ.get("DEPLOYING") == "1":
            print(f"  FAIL {msg}")
            print(f"::error::{msg}")
            print("\nFAIL: sample donate settings must not reach the live site")
            return 1
        print(f"  WARN {msg}")
        print(f"::warning::{msg}")
        if production:
            print("       a deploy to the live host will refuse this - set sample: false first")
        else:
            print("       fine on a staging build - set sample: false before this goes live")

    if enabled:
        url = s.get("provider.url", "")
        if not url.startswith("https://"):
            bad.append("enabled, but provider.url is not set to an https URL")
        if not s.get("amounts"):
            bad.append("enabled, but no preset amounts are set")
        pp = s.get("paypal.url", "")
        if pp and not pp.startswith("https://"):
            bad.append("paypal.url is set but is not an https URL")
        if not s.get("bank.iban") and not s.get("bank.email"):
            bad.append("no bank route: set either bank.iban or bank.email")
        if hidden or noindex:
            bad.append("enabled, but the page still carries hidden/noindex")
        if not sample and ("example.invalid" in url or "SAMPLE" in DATA.read_text()):
            bad.append("live settings still contain sample values")
        if url and url.split("{")[0] not in html:
            bad.append("enabled, but the built page links to no provider URL")
        # A donate page nobody can find is the other half of issue #18.
        found = linkers()
        print(f"pages linking to it  : {len(found)}")
        if "index.html" not in found:
            bad.append("enabled, but the homepage does not link to it")
        if not any(f.endswith("about/anbi/index.html") for f in found):
            bad.append("enabled, but the footer link is missing (checked on /about/anbi/)")
    else:
        if not hidden:
            bad.append("not enabled, but the page is not hidden from the menus")
        if not noindex:
            bad.append("not enabled, but the page is not noindex")
        if "notice" not in html:
            bad.append("not enabled, but the page shows no notice saying so")
        found = linkers()
        if found:
            bad.append(f"not enabled, but {len(found)} page(s) link to it: {', '.join(found[:3])}")
        sm = ROOT / "public" / "sitemap.xml"
        if sm.exists() and "get-involved/donate" in sm.read_text():
            bad.append("not enabled, but the page appears in the sitemap")

    if not ALIAS.exists():
        bad.append("/donate/ does not resolve - the short URL is what goes in an email")

    for b in bad:
        print(f"  FAIL {b}")
        print(f"::error::donate page - {b}")
    print()
    print("FAIL: donate settings and page disagree" if bad else "PASS: donate page matches its settings")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
