# Contributing

This is a volunteer project. Most useful changes are a few lines of Markdown or
YAML, and you can make them in the GitHub web interface without installing
anything.

---

## The short version

1. Open an issue first for anything that changes what the site says, or how it
   is organised. Fixing a typo does not need one.
2. Branch from `main`, one topic per branch.
3. Open a pull request. Every check runs automatically.
4. Say what you verified, not only what you changed.

---

## Running it locally

You need **Hugo** and nothing else to build the site or change any of its
content. No credentials.

```bash
git clone https://github.com/csirt-global/website
cd website
make serve            # http://localhost:1313
```

`make serve` downloads the pinned Tailwind binary on first run (~76 MB, cached
in `bin/`, gitignored). Install Hugo with `brew install hugo` or from
[gohugo.io/installation](https://gohugo.io/installation/), matching the version
in `.hugo_version`.

```bash
make check            # everything CI runs
make build            # production build into public/
make clean            # remove build output
```

Run `make check` before opening a pull request. It builds first, so it catches
anything a template change broke.

---

## What goes where

| You want to | Edit |
|---|---|
| Fix wording on a page | `content/<page>/index.<lang>.md` |
| Change a heading, button or label | `i18n/<lang>.yaml` — not the template |
| Add or remove a team member | `data/team.yaml` |
| Add a case | `content/cases/CG-YYYY-NNNNN/` (`hugo new cases/...`) |
| Add a project | `content/projects/<slug>/` |
| Change a nav item | `data/nav.yaml` |
| Change the organisation record | `data/verify.yaml` |
| Add an ANBI document | `data/anbi_documents.yaml`, PDF in `static/uploads/` |
| Turn on donations | `data/donate.yaml` — see [docs/CONTENT.md](docs/CONTENT.md) |
| Change colours or type | `assets/css/main.css`, `@theme` block only |
| Change the logo | `assets/images/logo-mark.svg`, then `npm run favicons` |

**You should not need to touch HTML.** If a content change requires editing a
template, that is usually a sign the template should be reading from `data/`
instead. Say so in the issue.

Read [docs/CONTENT.md](docs/CONTENT.md) for the exact fields of each type, and
[docs/QUIRKS.md](docs/QUIRKS.md) before editing templates — it is a list of
things that have already gone wrong here.

---

## Pull requests

**One change per pull request.** A branch that fixes a broken link and also
redesigns the footer is two pull requests. Reviewers here are volunteers reading
in the evening; a small diff gets merged, a large one gets postponed.

**Title**: imperative mood, no ticket prefix, no full stop.

```
Fix mobile menu being clipped on sub-pages
Add the 2025 financial report to the ANBI page
```

Not `fixed menu bug`, not `Update index.html`.

**Description**: what changed, why, and how you know it works. If you fixed
something visual, say what you looked at. If you changed a URL, say what still
points at the old one.

**Do not** commit `public/`, `resources/`, `assets/css/build.css` or
`bin/tailwindcss`. They are generated and gitignored.

**Commit messages**: imperative subject, then a body explaining why. Check
`git config user.email` is the address you mean to commit under.

---

## What the checks enforce

`make check` and CI run the same things. All of them exist because something
went wrong once:

| Check | Guards against |
|---|---|
| `check-urls.py` | An ANBI document or a citable case URL disappearing |
| `check-links.py` | Broken internal links, and stray whitespace welded to a link |
| `check-css.py` | A component class used in a template with no rule in the stylesheet |
| `check-security-txt.py` | `/.well-known/security.txt` lapsing (RFC 9116) |
| `check-donate.py` | A donate page that is live with placeholder payment details |
| `check-content-parity.py` | Text from the previous site vanishing in a redesign |
| `translation-status.py` | The site quietly becoming English-only |

A failing check is telling you something. If you are certain it is wrong, say so
in the pull request rather than working around it — several of them have
exceptions lists that take a reason in writing.

`scripts/sweep.mjs` is not in CI, because it needs a running server and a real
browser. Run it by hand for anything that changes layout:

```bash
npm ci                           # once: Playwright, the only npm dependency
make serve                       # in one terminal
npm run sweep                    # in another
```

It checks 20 pages at 390/768/1440 for horizontal scroll, failed requests,
external links opening in the same tab, blocked pinch-zoom, and a visible
keyboard focus ring. CI runs it too, against the built artifact.

[docs/CI.md](docs/CI.md) explains what CI runs and how deployment works.

---

## Things that must not break

- `/cases/CG-YYYY-NNNNN/` — externally cited, and **case-sensitive**
- `/uploads/*.pdf` — statutory ANBI filings the Dutch tax authority relies on
- `/.well-known/security.txt` — RFC 9116
- `/code/`, and the old homepage anchors `#mission`, `#team`, `#code`, `#anbi`
- The Code of Conduct's 24 numbered clauses, which carry governance weight

`check-urls.py` enforces the first four.

---

## Translations

English first. A page is written in English, reviewed, and only then translated.

**Editing a page in one language means editing it in all of them.** A correction to a case record is
a correction in seven files. If a change genuinely does not apply elsewhere, put
`Translation-sync: not-required, <reason>` in the commit message rather than making six no-op edits.

**Every language at 100% is enforced by CI.** Today that is all five, so adding an English page means
adding its Dutch, German, French and Spanish versions in the same pull request, or the build fails.
A language still being written sits at `0.00` in `scripts/translation-status.py` and is only reported,
so adding a new language does not fail CI on day one. If a translation
genuinely cannot be written yet, add the file with `untranslated: true`: it renders with a notice
explaining why the reader is seeing English, and it counts as missing until it is real.

A `.<lang>.md` file that contains English text is worse than no file at all: it
reports as translated and reads as neglect. Mark it `untranslated: true` in the
front matter instead, and `translation-status.py` will count it as missing.

See [docs/TRANSLATION.md](docs/TRANSLATION.md).

---

## Reporting a security issue

Not through an issue. See [SECURITY.md](SECURITY.md).
