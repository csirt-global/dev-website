# Editing content

Every field below lives in Markdown or YAML. You never need to write HTML.

---

## Team members — `data/team.yaml`

The team page is generated from this file. Three groups: `supervisory`, `board`, `management`.

```yaml
- name: "Jane Doe"                       # shown as-is, not translated
  role: role_advisor                     # an i18n key, see below
  photo: images/jane.jpg                 # put the file in assets/images/
  anchor: jane                           # optional: gives the card an #jane id
  social:                                # optional, any number
    - { kind: x,        url: "https://twitter.com/janedoe" }
    - { kind: linkedin, url: "https://www.linkedin.com/in/janedoe/" }
    - { kind: mastodon, url: "https://infosec.exchange/@janedoe" }
    - { kind: email,    url: "mailto:jane@csirt.global" }
```

`kind` must be one of `x`, `linkedin`, `mastodon`, `email`. Each renders an icon at the same size.

**`role` is a translation key, not text.** Add it to every file in `i18n/` so the job title
translates. If a role does not exist yet, add for example `role_advisor: "Advisor"` to `i18n/en.yaml`
and the equivalent in the other languages.

**Do not add a social entry with a placeholder URL.** The previous site had two `href="#"` X icons
that looked like links and went nowhere. A missing icon is better than a dead one.

### Photos

Drop the original in `assets/images/`. It is resized to 224×224 and converted to WebP at build time,
so there is no need to shrink it first. A 7 MB photo becomes about 4 KB.

---

## Cases — `content/cases/<id>/index.<lang>.md`

One folder per case. The folder name is lowercase; `slug` sets the public URL and **must keep the
original capitalisation**, because case URLs are cited externally and are case-sensitive.

```yaml
---
title: "JetBrains TeamCity Authentication Bypass"
slug: "CG-2024-00001"                    # the URL: /cases/CG-2024-00001/
date: 2024-02-16                         # "Published"
lastmod: 2024-02-20                      # "Last updated", optional
case:
  id: "CG-2024-00001"
  status: closed                         # closed | current -> which list it appears in
  ref: "CG-2024-00001-teamcity"          # optional internal reference
  lead: "Soufian El Yadmani"
  leadAnchor: soufian                    # links to /#soufian
  researchers: ["Name One", "Name Two"]
  cve: ["CVE-2024-23917"]                # auto-linked to cve.org
  cwe:                                   # use instead of cve where relevant
    - { id: "CWE-538", label: "CWE-538: ...", url: "https://cwe.mitre.org/..." }
  product: "JetBrains TeamCity"
  productUrl: "https://www.jetbrains.com/teamcity/"
  cpe: "cpe:2.3:a:jetbrains:teamcity:*:*:*:*:*:*:*:*"
  vulnerableVersions: "23.9.7 and prior"
  vendorStatement: "https://..."
---

### Summary

Body text here.
```

Every field except `title`, `slug`, `date` and `case.id` is optional and simply not rendered if
absent. `status` decides whether the case appears under Current or Closed on `/cases/`; **the index
builds itself**, there is no link list to maintain.

Cases with no page of their own, only a CVE record, live in `data/external_cases.yaml`.

---

## Projects — `content/projects/<slug>/index.<lang>.md`

```yaml
---
title: "Global Universities (PGU)"
slug: "pgu"
weight: 1                                # ordering on /projects/
logo: "images/PGU.svg"
summary: "One line, shown on the projects index."
project:
  timeline:
    - year: "2025"
      body: "What happened. Markdown links work here."
  team:
    - { name: "...", role: "Project Lead", photo: "images/x.jpg", social: [ ... ] }
---

Body prose, then `## The Project` and so on.
```

Project team `role` is plain text, not an i18n key, because these titles are project-specific.

Partners are shared between projects and live in `data/partners.yaml`.

---

## Navigation — `data/nav.yaml`

```yaml
- key: nav_cases       # i18n key for the label
  url: "/cases/"
```

One list. It renders into both the desktop and mobile menus, in all five languages. A link whose
target has no translation in the current language falls back to English rather than 404ing.

---

## ANBI documents — `data/anbi_documents.yaml`

```yaml
- label: "CSIRT.global 2024 financieel verslag"
  url: "/uploads/CSIRT financieel verslag 2024.pdf"
```

Put the PDF in `static/uploads/`. **Do not rename existing files.** Two of them contain literal
spaces in the filename; those URLs are already published and referenced.

These are statutory publications the Dutch tax authority relies on. `scripts/check-urls.py` fails
the build if any of them stops resolving.

---

## The organisation record — `data/verify.yaml`

```yaml
rows:
  - key: "RSIN"
    value: "863825655"
  - key: "Legal entity"
    value: "Stichting CSIRT.global"
    url: "https://openkvk.nl/company/..."   # optional: makes the value a link
    note: "KvK register"                    # optional: greyed suffix
```

Rendered on the homepage, on `/notified/` and on `/about/anbi/`. Every row must be something a
stranger can check on a source that is not us. A claim we cannot point at a third party for does not
belong here — that is the whole point of the block.

---

## Donations — `data/donate.yaml`

The page at `/get-involved/donate/` (short URL `/donate/`) is built entirely from
this file, and ships switched off. Issue #18 asked for a donate button; the one
thing nobody could supply was the provider and the URL.

To turn it on:

1. Fill in `provider.url` (put `{amount}` where the preset amount goes, if the
   provider accepts one), and whatever else applies — `paypal.url`, `bank.iban`,
   `usage`.
2. Delete `hidden`, `noindex` and the `sitemap` block from
   `content/get-involved/donate/index.en.md`.

Both steps, or neither. `scripts/check-donate.py` fails the build on half of it,
because a live donate page with dead buttons is worse than no donate page.

A field left empty removes its section rather than rendering an empty one, so the
page never publishes a payment route that does not work.

---

## Homepage — `content/_index.<lang>.md`

The homepage is assembled by `layouts/index.html`: the hero, the organisation record, the three
strands of work and the three most recent cases all come from `i18n/` and `data/`. The Markdown body
of `_index.<lang>.md` supplies only the mission text at the bottom.

To change the hero line or a section heading, edit `i18n/<lang>.yaml`, not the Markdown.

These shortcodes are available in any page body:

```
{{< details summary="Bug Bounties" >}}
Collapsible content.
{{< /details >}}

{{< news >}}                    the Supascribe feed
{{< anbi-documents >}}          the document list from data/
{{< figure src="images/x.png" alt="..." >}}
```

Write internal links as `/cases/`, never as `/nl/cases/`. The render hook resolves them to the
current language, falling back to English where a page is not translated.
