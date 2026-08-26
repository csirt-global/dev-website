---
name: verify-changes
description: Verify a change to this site properly - build, run every check, and look at the affected pages in a real browser. Use before saying a change works, and before opening a pull request.
---

# Verifying a change

`make check` passing is not evidence a visual change is correct. Several
regressions here passed every check: a deleted CSS component, a menu rendering
below its own breakpoint, a stray space in front of every link on the site.

## 1. Build and run the checks

```bash
make check
```

This builds first, then runs every script CI runs plus `check-content-parity.py`.
Read the output. A failing check is telling you something; if you are certain it
is wrong, say so rather than working around it — several of them have exception
lists that take a written reason.

## 2. Look at what you changed

```bash
make serve      # http://localhost:1313
```

Open every page the change touches. Not the homepage as a proxy for the site.

## 3. If it touched layout or CSS

```bash
node scripts/sweep.mjs
```

20 pages at 390/768/1440: horizontal scroll, failed requests, external links
opening in the same tab, blocked pinch-zoom, visible keyboard focus ring. Then
the header in all seven languages at 1280 and 1440, printing the spare room.
Read those numbers: a language with single-digit headroom is one label away from
a wrapped menu, which is how French shipped broken.

It needs a running server. Do **not** run `make build` while `make serve` is up:
the build clears `public/` underneath the server and the site comes back looking
broken for reasons that have nothing to do with your change.

Playwright drives the installed Google Chrome via `channel: "chrome"`, because
its own cached browsers are stale. If `playwright` is not resolvable from the
repository, run it from a directory where it is installed:

```bash
cd /path/with/playwright && node /path/to/repo/scripts/sweep.mjs
```

## When taking screenshots

- **Scroll the page first.** Images below the fold are `loading="lazy"` and a
  full-page screenshot otherwise captures them as empty boxes.
- **Wait past the transition.** A dropdown captured mid-transition looks
  translucent. Read the computed style if unsure — it does not lie.

## Reporting the result

Say what you actually ran and what you actually looked at. "make check passes"
is a start, not an answer, for anything visual. If something is still broken,
say so with the output rather than hedging.
