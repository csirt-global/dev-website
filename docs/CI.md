# Continuous integration and deployment

Two workflows, both in `.github/workflows/`. Neither installs a package manager.

| Workflow | Runs on | Does |
|---|---|---|
| `ci.yml` | every pull request | Builds, runs every check, then drives a real browser over the result. |
| `deploy.yml` | pushes to `main`, or by hand | Rebuilds against the real domain, runs the checks against that artifact, and publishes it. |

**Everything that can be known before a merge is checked before a merge.** `ci.yml`
does not run on `main` at all: after a merge `deploy.yml` runs the same checks
against the artifact it is about to publish, so running them twice would only
mean waiting twice.

Only two things genuinely cannot happen earlier, and both live in `deploy.yml`:
building against the deployment's real `baseURL`, and publishing.

---

## What CI actually does

```
Verify Hugo pin matches .hugo_version     ← fails if the two disagree
Install Hugo <pinned>                     ← .deb from the GitHub release
Install Tailwind <pinned>                 ← standalone binary, no npm
Build CSS                                 ← make css
Build site                                ← hugo --gc --minify --printPathWarnings
Check required URLs still resolve         ← check-urls.py
Check translation coverage                ← translation-status.py
Check for broken internal links           ← check-links.py
Check translations were changed together  ← check-translation-sync.py
Check every component class has a rule    ← check-css.py
Check security.txt has not lapsed         ← check-security-txt.py
Check the donate page matches its settings← check-donate.py
Upload build

  ↓ browser job, reusing that artifact

Install Playwright                        ← 3 packages, pinned by the lockfile
Serve the build                           ← python3 -m http.server
Responsive and accessibility sweep        ← sweep.mjs
```

The browser job downloads the artifact the build job produced rather than
rebuilding, so it tests exactly what was built.

Both tool versions are pinned in the workflow `env` and, for Hugo, in
`.hugo_version` as well. The first step fails the build if those two disagree,
because a pin nobody notices has drifted is not a pin.

`timeout-minutes: 10` and a `concurrency` group are set so a branch that gets
three pushes in a minute does not run three builds.

---

## Running the same thing locally

```bash
make check
```

That builds first and then runs every script CI runs, plus
`check-content-parity.py`, which CI skips. Parity compares against a local build
of the previous site; CI has no copy of it, and the script exits cleanly when the
reference is absent.

The browser sweep is separate, because it needs a running server and a browser:

```bash
npm ci                           # once; Playwright, pinned by package-lock.json
make serve                       # terminal 1
npm run sweep                    # terminal 2
```

`sweep.mjs` drives 20 pages at 390/768/1440 and checks for horizontal scroll,
failed requests, external links opening in the same tab, blocked pinch-zoom, and
a visible keyboard focus ring. It then measures the header in all seven
languages at 1280 and 1440 and prints the spare room, which is what stops a new
language quietly breaking the menu. `BASE_URL` overrides the target, which is
how CI points it at a static server over the built artifact.

Playwright is the repository's only npm dependency and it never reaches the
site: Hugo and Tailwind build the pages, this only looks at them. Editing
content needs none of it.

---

## Why the checks are scripts

Every one of them encodes something specific to this organisation that a
general-purpose tool has no way to know:

- that `/uploads/CSIRT financieel verslag 2022.pdf` must never 404, because the
  Dutch tax authority relies on it
- that `/cases/CG-2024-00001/` is case-sensitive and externally cited
- that a `.nl.md` file full of English is worse than no file at all
- that a donate page with placeholder payment details must not reach the live
  site

They are also the reason `make check` and CI test the same thing. A check that
only exists inside a workflow cannot be run before pushing.

The trade is real: about 1,100 lines of Python with no tests of their own, and a
buggy check gives false confidence. Two already have. `check-donate.py` read
`hidden: true` out of a comment that explained how to restore `hidden: true`.
`translation-status.py` split words on a character class containing no Han, so a
correct Chinese page scored 100% English and failed the build.

When you add a check, prove it fails on the thing it is meant to catch before
trusting that it passes. And know what it cannot see: `check-content-parity.py`
only inspects text blocks over 30 characters, so it says nothing about a name
being removed from the team page.

---

## Adding a check

1. Write `scripts/check-<thing>.py`. Module docstring first, saying what went
   wrong that made the check necessary.
2. Print a summary, then one `::error::` line per failure so GitHub annotates
   the diff. Exit non-zero.
3. Break the thing on purpose and confirm it fails. Then fix it and confirm it
   passes.
4. Add it to `check:` in the `Makefile` and to `ci.yml`. Both, or it is a check
   that cannot be run before pushing.
5. Add a row to the table in `README.md` saying where it runs and what it guards
   against, and to the shorter table in `CONTRIBUTING.md`.

---

## Deployment

`deploy.yml` publishes to GitHub Pages using
`actions/configure-pages` → `actions/upload-pages-artifact` →
`actions/deploy-pages`. Permissions are the minimum those need:
`contents: read`, `pages: write`, `id-token: write`.

The build is passed `--baseURL` from `configure-pages`, which resolves to
whatever custom domain that repository has configured. Everything downstream
follows from it.

### The published site is checked after it is published

Every check in the build job reads `./public`, the folder Hugo wrote. That is
not the same thing as what visitors get: the artifact upload sits between them
and can drop files.

That is not hypothetical. `actions/upload-pages-artifact` v4 stopped including
hidden files, which would have removed `/.well-known/security.txt` from the
published site. `check-urls.py` would still have passed, because the file was
there in `./public`. The deploy would still have reported success. Only the live
URL would have been wrong.

So `check-deployed.py` runs after `deploy-pages` and fetches real URLs over the
network: the ANBI documents, every citable page, `security.txt` including its
`Contact:` line, and a lowercased case URL that must **not** resolve. The list is
imported from `check-urls.py` rather than repeated, so the build and the
published site are held to the same one.

It detects rather than prevents. By the time it runs the site is live, so a red
deploy is the alarm and reverting the commit republishes.

### The domain is a repository setting, not a file

There is deliberately **no `CNAME` file in this repository.** The same source is
deployed to more than one hostname, and a committed `CNAME` would make a staging
deploy claim the live domain — GitHub would then have two repositories asserting
`csirt.global`.

Set the custom domain in **Settings → Pages** for each repository. The deploy
workflow reads it back from `configure-pages` and writes `public/CNAME` into the
artifact from that, so each repository publishes its own domain and neither can
claim the other's. A `*.github.io` base URL means no custom domain is set, and
then nothing is written.

### Anything that is not the live site marks itself

`hugo.yaml` names one `productionHost`. A build whose `baseURL` host is anything
else is treated as a copy, and:

- every page gets `<meta name="robots" content="noindex, nofollow">`
- `robots.txt` becomes `Disallow: /`
- a banner appears at the top of every page pointing at the live site
- `check-donate.py` allows sample payment settings, which it refuses on a
  deploy to the live host

This matters more here than on most sites. A public copy of a security
organisation's website, on a hostname that is not the one we tell people to
check, is a lookalike of that organisation. It should be impossible to mistake
for the real thing, and impossible to find by search.

Localhost is exempt from the banner only — the person running the server knows
what they are looking at.

### Sample settings

The donate page currently ships **switched on with sample settings**, so the
design can be reviewed before anyone has picked a payment provider. Every route
on it points at `example.invalid`, a reserved domain that cannot resolve, and
the page carries a banner saying so.

`check-donate.py` warns about that everywhere and refuses it in exactly one
place: a deploy whose target is the live host. Nothing else publishes, so
nothing else needs to refuse. `deploy.yml` sets `DEPLOYING=1` on its check step;
a local build and a pull request both build against the default `baseURL`, which
is the live host, but neither of them publishes anything.

| Where | Sample settings |
| --- | --- |
| Local build | Warn |
| Pull request | Warn, annotated on the diff |
| Deploy to `staging.csirt.global` | Warn |
| Deploy to `csirt.global` | **Refused** |

To hand it over: fill in `data/donate.yaml` and set `sample: false`.

### Deploying to staging

`csirt-global/dev-website` is public, uses `build_type: workflow`, and has
`staging.csirt.global` configured. Pushing this repository's `main` there
deploys to that hostname with the whole not-production treatment applied.
