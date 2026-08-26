# csirt.global

The CSIRT.global website. Static site, built with [Hugo](https://gohugo.io), deployed by GitHub
Actions to GitHub Pages.

Available in English, Dutch, German, French and Spanish.

---

## Quick start

You need **nothing installed except Hugo**. There is no `npm install`, no `node_modules`, and no
credentials.

```bash
git clone <this repo>
cd website
make serve            # http://localhost:1313
```

`make serve` downloads the pinned Tailwind binary on first run (about 76 MB, cached in `bin/`),
builds the stylesheet, and starts Hugo with live reload.

If you do not have Hugo, install it with `brew install hugo` (macOS) or see
[gohugo.io/installation](https://gohugo.io/installation/). Use the version in `.hugo_version`.

### Commands

| command | what it does |
|---|---|
| `make serve` | local preview with live reload |
| `make build` | production build into `public/` |
| `make check` | run every check CI runs |
| `make css` | rebuild the stylesheet only |
| `make clean` | remove build output |
| `npm ci && npm run sweep` | browser sweep: 20 pages x 390/768/1440 (needs `make serve` running) |

---

## Editing content

Everything a person normally changes lives in `content/` (prose) or `data/` (structured lists).
**You do not need to touch HTML.**

- **Add a team member** → edit `data/team.yaml`
- **Add a case** → add a folder under `content/cases/`
- **Add a project** → add a folder under `content/projects/`
- **Change a nav item** → edit `data/nav.yaml` (once, not eight times)
- **Change an ANBI document** → edit `data/anbi_documents.yaml`
- **Turn on donations** → fill in `data/donate.yaml`, then remove `hidden`/`noindex`/`sitemap` from `content/get-involved/donate/index.en.md`
- **Change wording on the homepage** → edit `content/_index.<lang>.md`

You can edit these files directly in the GitHub web interface. Opening a pull request runs every
check automatically.

| Document | What is in it |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to run it, what goes where, pull request standards |
| [docs/CONTENT.md](docs/CONTENT.md) | The exact fields of every content type |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Why it is built this way, decision by decision |
| [docs/QUIRKS.md](docs/QUIRKS.md) | Traps that have already caught someone here. Read before editing templates or CSS |
| [docs/CI.md](docs/CI.md) | The two workflows, what each check guards, how the domain and staging work |
| [docs/TRANSLATION.md](docs/TRANSLATION.md) | How the five languages work |
| [CLAUDE.md](CLAUDE.md) | Rules and context for contributors working with Claude Code |
| [SECURITY.md](SECURITY.md) | Reporting a vulnerability in this site |

---

## How the site is organised

The old site was one page: an 11-screen homepage carrying about two thirds of all the words on the
site, with the governance and ANBI material at the very bottom. This version splits it up around who
actually arrives.

The most common visitor is not browsing. They have just received an unsolicited email saying a
system they own is vulnerable, and they are trying to work out whether it is a scam. `/notified/`
answers exactly that, and it is the first item in the navigation. The second audience, funders and
press assessing legitimacy, wants the same thing: facts they can check without taking our word for
it. Both are served by the organisation record — legal entity, RSIN, registered office, ANBI status,
`security.txt`, the case register — which appears on the homepage, on `/notified/` and on
`/about/anbi/`, rendered from `data/verify.yaml`.

```
/                       what we are, why you may have heard from us, proof
/notified/              "you received an email from us"
/what-we-do/            bug bounties, exploit research, incident response
/cases/                 the case register, one page per case
/projects/              PGU, PGNGO
/about/                 team, code of conduct, ANBI
/get-involved/          volunteering and open roles
/news/
```

Every URL the old site served still resolves. Old homepage anchors (`#mission`, `#team`, `#code`,
`#anbi`) redirect to their new pages, so existing inbound links keep working.

---

## How this is put together

```
assets/css/main.css       brand tokens + Tailwind entry point
assets/images/            images processed at build time (resized, WebP)
content/                  the words, as Markdown, one file per language
data/                     structured lists: nav, team, partners, documents
i18n/                     interface strings per language
layouts/                  templates (the only place HTML lives)
scripts/                  the checks CI runs
static/                   files served as-is: favicons, PDFs, security.txt
.github/workflows/        build, check, deploy
```

Two principles worth knowing, because they are why the previous version drifted:

**Everything shared exists once.** The navigation, the team, the partner list, the page header. The
previous site copy-pasted its ~128-line header into 8 files; the copies drifted into five variants
with different nav items, and fixing them meant editing all eight.

**Nothing built is committed.** CSS and resized images are produced by the build. The previous site
committed its compiled stylesheet, which then went 2.5 years without a rebuild while pages kept
being added, so 17 CSS classes used on live pages did not exist in the stylesheet being served.

---

## Checks

`make check`, and CI on every pull request:

| check | why it exists |
|---|---|
| `scripts/check-urls.py` | The ANBI contact details and documents must stay reachable for the Dutch tax authority (Belastingdienst). Also guards case URLs, which are case-sensitive and cited externally. |
| `scripts/check-links.py` | The previous site shipped a link with no scheme that 404'd, and a logo pointing at a deleted third-party asset. Both were live for months. Also catches stray whitespace welded to a link, which is what an untrimmed newline in a render hook turns into on the page. |
| `scripts/translation-status.py` | Five languages fail silently: Hugo falls back to English, so an untranslated page looks fine to anyone who does not read that language. This makes the gap countable. |
| `scripts/check-security-txt.py` | RFC 9116 makes `Expires` mandatory and says a lapsed file must not be relied on. The previous one expired on 2025-01-01 and stayed published for over a year (issue #56). This fails 30 days ahead. |
| `scripts/check-css.py` | Component classes are hand-written, so deleting one while editing leaves every template that uses it silently unstyled. That happened here: a splice removed the case record block and the register rendered as plain text for three commits. |
| `scripts/check-donate.py` | The donate page ships switched off until someone supplies a provider and a URL (issue #18). Two things have to move together to switch it on, and doing one without the other gives either a live page nobody can reach or a reachable page with buttons that go nowhere. This refuses both. |
| `scripts/check-content-parity.py` | The redesign moved every page. This asserts that no sentence the old site published was lost on the way. A drop has to be written down in `ALLOWED_DROPS` with a reason, so losing content is a decision rather than an accident. Skips when the reference build is not present. |
| `scripts/sweep.mjs` | Every page at 390/768/1440: no horizontal scroll, no failed requests, every external link opening in a new tab, pinch-zoom not blocked, a visible keyboard focus ring. Needs a local server and Playwright, so it is run by hand rather than in CI. |

`check-content-parity.py` runs in `make check` but not in CI: it compares against
a local build of the previous site, which CI does not have, and skips cleanly
when that is absent.

---

## Deployment

Pushing to `main` builds and deploys to GitHub Pages. The build is reproducible: Hugo and Tailwind
versions are pinned in `.hugo_version` and the workflow, and CI fails if they disagree.

Do not commit `public/`, `resources/` or `static/css/main.css`. They are generated.

---

## Things that must not break

- `/cases/CG-2024-0000N/` — externally cited, **case-sensitive**
- `/uploads/*.pdf` — statutory ANBI filings, legally required to stay published
- `/.well-known/security.txt` — RFC 9116
- `/code/` — redirect kept because the Code of Conduct used to live there
- The `#mission`, `#team`, `#code`, `#anbi` anchors — linked from other pages and externally
- The custom domain is a **repository setting**, not a file. There is no `CNAME`
  in this repository on purpose: the same source deploys to more than one
  hostname, and a committed one would make a staging deploy claim the live
  domain. See [docs/CI.md](docs/CI.md).
- Internal links go through `layouts/partials/href.html`, which points at the translation when one
  exists and at the English page when it does not. Writing `/nl/…` by hand produces a 404 the day
  that page is not translated.

`scripts/check-urls.py` enforces these.
