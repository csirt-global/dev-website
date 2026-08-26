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

**`role` is a translation key, not text.** If a role does not exist yet, add for example
`role_advisor: "Advisor"` to `i18n/en.yaml`. Job titles stay in English in every language, so
`i18n/en.yaml` is the only file that carries `role_` keys: do not add them to the others, and do not
translate the ones that are there.

**Do not add a social entry with a placeholder URL.** The previous site had two `href="#"` X icons
that looked like links and went nowhere. A missing icon is better than a dead one.

### Photos

Drop the original in `assets/images/`. It is resized to 224×224 and converted to WebP at build time,
so there is no need to shrink it first. A 7 MB photo becomes about 4 KB.

---

## Cases

A case is **two files**, and the second one is the part people forget.

### 1. The facts — `data/cases/<slug>.yaml`

```yaml
id: "CG-2024-00001"
ref: "CG-2024-00001-teamcity"            # optional internal reference
status: closed                           # closed | current -> which list it appears in
lead: "Soufian El Yadmani"
leadAnchor: soufian                      # their anchor on /about/team/
researchers: ["Name One", "Name Two"]
cve: ["CVE-2024-23917"]                  # auto-linked to cve.org
cwe:                                     # use instead of cve where relevant
  - { id: "CWE-538", label: "CWE-538: ...", url: "https://cwe.mitre.org/..." }
product: "JetBrains TeamCity"
productUrl: "https://www.jetbrains.com/teamcity/"
cpe: "cpe:2.3:a:jetbrains:teamcity:*:*:*:*:*:*:*:*"
vulnerableVersions: "23.9.7 and prior"
vendorStatement: "https://..."
```

None of this is language-dependent. A CVE, a CPE string and a researcher's name are the same in
every language, so they exist once here rather than seven times. **The build fails with an error
naming this file if it is missing**, so a case cannot ship without its facts.

### 2. The prose — `content/cases/<id>/index.<lang>.md`

One folder per case, one file per language. The folder name sets `slug`, which sets the public URL,
and it **must keep the original capitalisation**, because case URLs are cited externally and are
case-sensitive.

```yaml
---
title: "JetBrains TeamCity Authentication Bypass"
slug: "CG-2024-00001"                    # the URL: /cases/CG-2024-00001/
date: 2024-02-16                         # "Published"
lastmod: 2024-02-20                      # "Last updated", optional
---

### Summary

Body text here.
```

Every field in the data file except `id` and `status` is optional and simply not rendered if absent.
`status` decides whether the case appears under Current or Closed on `/cases/`; **the index builds
itself**, there is no link list to maintain.

A translation may add a `case:` block to its own front matter to override a single field that
genuinely carries prose. `vulnerableVersions: "23.9.7 and prior"` has an English tail, and the Dutch
page rightly says "en ouder". Everything not named in that block still comes from the one data file.

`hugo new cases/CG-YYYY-NNNNN/index.en.md` writes the prose file with the right `slug`. It cannot
write the data file; copy an existing one.

Cases with no page of their own, only a CVE record, live in `data/external_cases.yaml`.

---

## Projects — `content/projects/<slug>/index.<lang>.md`

Like a case, a project is two files: the people in `data/`, the words in `content/`.

```yaml
# content/projects/pgu/index.<lang>.md
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
  teamHeading: "The team"
  teamIntro: |
    Prose above the team cards.
---

Body prose, then `## The Project` and so on.
```

```yaml
# data/projects/pgu.yaml
team:
  - name: "Jane Doe"
    role: role_project_lead              # an i18n key, same as data/team.yaml
    photo: "images/jane.jpg"
    social:
      - { kind: linkedin, url: "https://www.linkedin.com/in/janedoe/" }
```

The team is in `data/` for the same reason the case facts are: a name, a photo and a LinkedIn URL
are identical in every language, and repeating the block in seven files is how one of those URLs
quietly ends up wrong. `timeline` and `teamIntro` stay in the front matter because they are prose.

Partners are shared between projects and live in `data/partners.yaml`.

---

## Navigation — `data/nav.yaml`

```yaml
- key: nav_cases       # i18n key for the label
  url: "/cases/"
```

One list. It renders into both the desktop and mobile menus, in all seven languages. A link whose
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
this file. Issue #18 asked for a donate button; the one thing nobody could
supply was the provider and the URL.

It is currently **switched on with sample settings**, so the design can be
reviewed before anyone picks a provider. Every route on it points at
`example.invalid`, a reserved domain that cannot resolve, and the page says so.

To hand it over:

1. Fill in `provider.url` (put `{amount}` where the preset amount goes, if the
   provider accepts one), and whatever else applies — `paypal.url`, `bank.iban`,
   `usage`.
2. Set `sample: false` in the same file.

`scripts/check-donate.py` warns about sample settings everywhere and refuses
them in exactly one place: a deploy whose target is the live host. It also
refuses `sample: false` while the values are still placeholders. See
[CI.md](CI.md) for the full table.

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
