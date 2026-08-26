---
name: add-a-case
description: Add a vulnerability case record to the case register at /cases/. Use when publishing a new CG-YYYY-NNNNN case, including its metadata, CVEs and researchers.
---

# Adding a case

Case URLs are externally cited and **case-sensitive**. `/cases/CG-2024-00001/`
must not become `/cases/cg-2024-00001/`; it would 404 on GitHub Pages while
looking fine on macOS.

## 1. Create it

```bash
hugo new cases/CG-2026-00004/index.en.md
```

The archetype produces the right front matter. Fill it in:

```yaml
title: "Vendor Product Authentication Bypass"   # no CVE, no case id in the title
slug: "CG-2026-00004"                           # keep the capitals
date: 2026-08-26
case:
  id: "CG-2026-00004"
  ref: "CG-2026-00004-vendor-product"
  status: current                                # current | closed
  lead: "Name"
  leadAnchor: firstname                          # their anchor on /about/team/
  researchers: ["Name", "Name"]
  cve: ["CVE-2026-00000"]
  product: "Product"
  productUrl: "https://vendor.example/product"
```

The CVE and the case id render as their own record fields, so repeating them in
the title duplicates them on every row of the register.

## 2. Write the body

What the vulnerability is, who is affected, what owners should do. Vendor
statements and updates belong in the body, not the front matter.

Write internal links as `/cases/`, never `/nl/cases/` — the render hook resolves
them per language.

## 3. Verify

```bash
make check
```

`check-urls.py` will confirm the URL resolves with its capitals intact. Then
look at `/cases/` and the case page itself: the register groups by
`case.status`, so a wrong status puts it under the wrong heading.

## Facts are not editable

Case record facts — dates, CVEs, researcher names, vendor statements — are not
copy. Do not tidy them, reword them, or fill a gap with something plausible. If
a field is unknown, leave it out and say so.
