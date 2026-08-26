# Working on this repository with Claude Code

The website of [CSIRT.global](https://csirt.global), a volunteer-led
not-for-profit foundation that finds vulnerabilities in public systems and
notifies the owners.

Read [CONTRIBUTING.md](CONTRIBUTING.md) first for what goes where, and
[docs/QUIRKS.md](docs/QUIRKS.md) before editing any template or CSS — it is a
list of things that have already gone wrong in this codebase, with symptoms.

---

## Hard rules

**Check `git config user.email` resolves to the contributor** before the first
commit in a clone. Commits should carry the identity of the person responsible
for them.

**Never push, open a pull request, or comment on an issue without being asked
for that specific action.** Local branches and commits are fine unprompted.
Approval for one push does not carry to the next.

**The ANBI material is a legal obligation.** `/uploads/*.pdf` and the details in
`data/verify.yaml` are published because the Dutch tax authority requires it.
Do not rename, move or edit them outside an explicit request.

**Copy is not yours to rewrite.** Fix an obvious typo silently; anything that
changes what the organisation says or commits to gets proposed, not applied. The
Code of Conduct's 24 numbered clauses and case record facts are untouchable.

**English first.** A translated file containing English text is worse than a
missing one: it reports as done and reads as neglect. Mark it
`untranslated: true` and let `translation-status.py` count it as missing.

---

## Before you say something works

Run the checks and look at the page. Both.

```bash
make check                       # builds, then runs every check
make serve                       # then look at what you changed
node scripts/sweep.mjs           # if it touched layout or CSS
```

`make check` passing is not evidence that a visual change is correct. Several
regressions in this repository's history passed every check: a deleted CSS
component, a menu that rendered below its own breakpoint, a stray space in front
of every link.

**When you add a check, break the thing first.** Confirm it fails on the case it
exists for, then fix it and confirm it passes. A check that has only ever passed
has not been tested.

**Screenshots lie.** Lazy-loaded images below the fold appear empty, and panels
captured mid-transition appear translucent. Scroll and wait, or read the
computed style, before calling either a bug.

**Open the evidence.** If someone attached a screenshot to an issue, open it.
Two of three issues in this repository's history were diagnosed wrongly from
their titles alone.

---

## How the site is structured

```
content/       the words, Markdown, one file per language
data/          structured lists: nav, team, partners, ANBI documents,
               the organisation record, donation settings
i18n/          interface strings per language — headings and labels live here,
               not in templates
layouts/       the only place HTML exists
assets/css/    main.css: an @theme token block, then hand-written components
scripts/       the checks
static/        served as-is: PDFs, fonts, favicons, security.txt
```

Two principles the whole repository rests on:

**Everything shared exists once.** The nav, the team, the page header, the
organisation record. The previous site copy-pasted a 128-line header into eight
files and the copies drifted into five variants.

**Nothing generated is committed.** CSS and resized images are build outputs.
The previous site committed its compiled stylesheet, which then went 2.5 years
without a rebuild while pages kept being added.

If a content change requires editing a template, that is usually a sign the
template should read from `data/` instead. Say so rather than hard-coding it.

---

## Design system

Brand colours are fixed: near-black `#1d1d1b` and the gold `#e1cd03`, which
is the gold in the logo mark itself.

- **The yellow is a signal**, not a wash: actions, case status, the support
  band. Never a large field of colour except that one band, which is the only
  inverted surface on the site.
- **Paper (`--color-paper`) means "a document you can check"**: the organisation
  record, `/notified/`, the ANBI filings. Ink is the site talking; paper is
  evidence.
- **Three type roles**: Archivo for display, IBM Plex Sans for body, IBM Plex
  Mono for identifiers. CVE numbers, case ids and the RSIN are identifiers and
  should look like them.

Every colour and type value resolves in the `@theme` block of
`assets/css/main.css`. Templates reference tokens, never literal hex.

Component classes are hand-written, so deleting one leaves every template that
uses it silently unstyled. `check-css.py` catches that; it exists because it
already happened.

---

## Who the site is for

Two audiences, and they want the same thing.

**Someone who just received an unsolicited email** saying a system they own is
vulnerable, trying to work out whether it is a scam. `/notified/` is for them
and is first in the navigation.

**Funders, partners and press** assessing whether the organisation is real.

Both want verifiable credibility, fast. That is why the organisation record —
RSIN, KvK, registered office, ANBI status, `security.txt`, the case register —
appears on the homepage, on `/notified/` and on `/about/anbi/`, and why nothing
on this site should make a claim it cannot point at a third party for.
