---
name: translate-a-page
description: Translate a page or interface string into Dutch, German, French or Spanish, following this repository's English-first rule. Use when adding or updating any non-English content.
---

# Translating a page

The site is English first. A page is written in English, reviewed, and only then
translated.

## The rule that matters

**A `.<lang>.md` file containing English text is worse than no file at all.** It
reports as translated, so nobody ever fixes it, and a reader in that language
gets a page that looks neglected rather than absent.

If you cannot translate it properly, mark it and move on:

```yaml
---
title: "..."
untranslated: true
---
```

`translation-status.py` counts that as missing, which is the truth.

## Where the words live

| What | Where |
|---|---|
| Page prose | `content/<page>/index.<lang>.md` |
| Headings, labels, buttons | `i18n/<lang>.yaml` — the same key in all five files |
| Team roles | `i18n/<lang>.yaml`; `data/team.yaml` holds the key, not the text |
| Names, photos, case facts | Not translated |

Adding an interface string means adding the key to **all five** `i18n` files.
English in the other four is the failure mode above, in a smaller box.

## Links

Write `/cases/`, never `/nl/cases/`. `layouts/partials/href.html` resolves an
internal link to the translation when one exists and to the English page when it
does not, so a hand-prefixed link becomes a 404 the day that page is not
translated.

## Check it

```bash
make check
```

`translation-status.py` prints per-language coverage and lists what is missing
or marked untranslated. `check-links.py` catches links that now point nowhere.

Then open the page in that language and read it. Machine-shaped Dutch is
noticeable to Dutch readers, and this organisation is Dutch.
