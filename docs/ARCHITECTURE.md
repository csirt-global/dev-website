# Architecture

Decisions worth knowing, and why they were made this way.

## Hugo, and only Hugo

A single pinned binary. There is no `npm install`, no `node_modules`, no lockfile to keep patched.

This matters because the site is dormant for months at a time. Between August 2025 and August 2026 the
previous repo received nine commits. A dependency tree that needs monthly security patches is a
liability on a repo nobody is watching: the sister site has 77 Dependabot commits and its four most
recent commits are security autofixes.

Tailwind also ships a standalone binary, so the whole toolchain is two pinned executables.

## Versions are pinned, and CI enforces the pin

`.hugo_version` and the workflow `env` must agree; CI fails if they drift. This is a direct response
to a site that pins nothing, uses `hugo-version: latest` and `npm install` rather than `npm ci`, and
can therefore break because a dependency shipped a release on a Tuesday.

## Nothing generated is committed

CSS and resized images are build outputs. The previous site committed its compiled stylesheet, which
then went 2.5 years without a rebuild while pages were still being added, so 17 utility classes used
on live pages simply did not exist in the stylesheet being served. Nobody noticed, because nothing
checked.

## Everything shared exists once

The nav is `data/nav.yaml`. The header is one partial. The team is `data/team.yaml`. Partners are
`data/partners.yaml`.

The previous site copy-pasted a ~128-line header into 8 files. Those copies drifted into five
variants: some pages were missing News, some were missing Projects, four had a malformed `</head  >`,
three rendered a stray backtick, and one project page carried the other project's title. Every one of
those was a symptom of there being no single place to edit.

## Brand values are tokens

`assets/css/main.css` defines every colour, font and radius in one `@theme` block. Templates
reference tokens, never literal hex values.

A corporate identity refresh has been raised as a future step. When it happens it should be an edit to
that block plus a few layouts, not a search-and-replace across every template.

The previous site declared Nunito in its Tailwind config but never loaded the font, so it has always
rendered in system fonts. This site loads three faces deliberately, and self-hosts them:

- **Archivo** for display. Heavy and slightly condensed, echoing the weight of the logo badge.
- **IBM Plex Sans** for body text. Built for technical documentation and comfortable at the sizes
  this content needs; the Code of Conduct alone is 24 numbered clauses.
- **IBM Plex Mono** for identifiers. CVE numbers, CPE strings, case numbers and the RSIN are
  identifiers and should look like identifiers.

They are served from `static/fonts/` rather than from Google Fonts. Embedding Google Fonts transmits
visitor IP addresses to a third party, which German courts have held breaches the GDPR. Our primary
audience is EU organisations deciding whether we are trustworthy, and a surveillance request on that
page would be a poor answer. All four files together are 116 KB.

## The yellow is a signal, and there is a paper surface

The brand is fixed: near-black `#1d1d1b` and the yellow `#f6e714`. What changed is how they are
used. The yellow is now reserved for actions, case status and the organisation record, never for
large fields of colour.

The departure is `--paper`, a light surface used for governance, ANBI and verification content. The
old site was black end to end, which reads as hacker aesthetic at exactly the moment our most common
visitor is asking "is this a scam?". On paper, that material reads as a document rather than a
landing page.

## Internal links resolve through one partial

`layouts/partials/href.html` takes a path and returns the translation of that page when one exists,
and the English page when it does not. The nav, the footer and the markdown render hook all go
through it.

The alternative — `relLangURL`, or writing `/nl/…` by hand in the markdown — emits a URL for a page
that may not exist in that language. That produced 72 broken links across the four translated sites
before this rule existed, all of them invisible to anyone reading English.

## Images are processed at build time

Originals go in `assets/images/`; Hugo resizes and converts to WebP. The previous site served
`soufian.jpg` at 6.98 MB for a 224-pixel avatar, which was 65% of all its image weight. The same
photo here is about 4 KB.

## URL case is preserved

`disablePathToLower: true`. Hugo lowercases paths by default, which would turn
`/cases/CG-2024-00001/` into `/cases/cg-2024-00001/`. GitHub Pages is case-sensitive, so that would
break an externally cited URL — and it would look fine on macOS, whose filesystem is not.

`scripts/check-urls.py` guards it explicitly.

## Third-party embeds

Kept, because the content genuinely lives there: **Supascribe** (news), **JotForm** (`/join/`),
**GoatCounter** (analytics), **Zerocopter** (`security.txt`).

Alpine.js is pinned to an exact version with a subresource integrity hash. The previous site loaded
`https://unpkg.com/alpinejs` with no version and no integrity check on all 8 pages, so whatever the
CDN served executed with full access to the page.

One consequence worth stating: these embeds are English-only. An English form inside a French page
undercuts the i18n goal, and is worth revisiting.
