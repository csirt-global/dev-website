---
name: add-a-case
description: Add a vulnerability case record to the case register at /cases/. Use when publishing a new CG-YYYY-NNNNN case, including its metadata, CVEs and researchers.
---

# Adding a case

Case URLs are externally cited and **case-sensitive**. `/cases/CG-2024-00001/`
must not become `/cases/cg-2024-00001/`; it would 404 on GitHub Pages while
looking fine on macOS.

A case is **two files.** Creating only the first one fails the build.

## 1. The facts — `data/cases/CG-2026-00004.yaml`

```yaml
id: "CG-2026-00004"
ref: "CG-2026-00004-vendor-product"
status: current                                  # current | closed
lead: "Name"
leadAnchor: firstname                            # their anchor on /about/team/
researchers: ["Name", "Name"]
cve: ["CVE-2026-00000"]
product: "Product"
productUrl: "https://vendor.example/product"
```

None of this is language-dependent, so it exists once here rather than seven
times. Copy an existing file in `data/cases/` and edit it. If this file is
missing the build stops with an error naming it.

## 2. The page — `content/cases/CG-2026-00004/index.en.md`

```bash
hugo new cases/CG-2026-00004/index.en.md
```

The archetype takes `slug` from the folder name and leaves `title` empty. Write
one:

```yaml
title: "Vendor Product Authentication Bypass"   # no CVE, no case id in the title
```

The CVE and the case id render as their own record fields, so repeating them in
the title duplicates them on every row of the register.

## 3. Write the body

What the vulnerability is, who is affected, what owners should do. Vendor
statements and updates belong in the body, not the front matter.

Write internal links as `/cases/`, never `/nl/cases/` — the render hook resolves
them per language.

## 4. Verify

```bash
make check
```

`check-urls.py` will confirm the URL resolves with its capitals intact. Then
look at `/cases/` and the case page itself: the register groups by `status`, so
a wrong status puts it under the wrong heading.

A case is a page like any other, so **it needs its six translations in the same
pull request** or `check-translation-sync.py` fails. Only the prose is
translated; the facts file is never translated.

## Facts are not editable

Case record facts — dates, CVEs, researcher names, vendor statements — are not
copy. Do not tidy them, reword them, or fill a gap with something plausible. If
a field is unknown, leave it out and say so.
