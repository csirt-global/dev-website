# Translations

The site ships in five languages: **English** (default), **Dutch**, **German**, **French** and
**Spanish**.

English lives at the site root (`/cases/`), the others under a prefix (`/nl/cases/`). That is
deliberate: existing URLs like `/cases/CG-2024-00001/` are cited externally and must not move.

---

## The failure mode this is built to avoid

Hugo falls back to the default language when a translation is missing. A page nobody translated
therefore looks completely fine — to anyone who does not read that language.

Our sister organisation's site shows where that leads: full i18n machinery, an `.en.md` suffix on all
66 content files, a language switcher rendered twice, two CMS configs declaring `[en, nl]`, a build
script looping over both locales, and an `.htaccess` rule redirecting `/nl` away. **Zero pages are
translated.** Meanwhile their genuinely Dutch content sits in files marked English.

So here, missing translations are made loud rather than silent:

- `scripts/translation-status.py` reports coverage per language and lists every missing page
- pages served in a language they were not translated into show a visible notice
- the language dropdown marks languages this page does not exist in, instead of silently linking

---

## Two kinds of text

**Interface strings** — nav labels, button text, section headings. These live in `i18n/<lang>.yaml`
as key/value pairs and are shared by every page.

```yaml
nav_cases: "Cases"
case_lead: "Case lead"
```

**Page content** — prose. One Markdown file per language, distinguished by the suffix:

```
content/_index.en.md
content/_index.nl.md
content/cases/cg-2024-00001/index.en.md
content/cases/cg-2024-00001/index.nl.md
```

Job titles and group names are interface strings, not page content, so they translate once and apply
everywhere. That is why `data/team.yaml` stores `role: role_advisor` rather than `role: "Advisor"`.

---

## Adding a translation

1. Copy the English file, change the suffix: `index.en.md` → `index.de.md`
2. Translate the body **and** the `title` and `description` in the front matter
3. Leave structural values alone: `slug`, `date`, `weight`, and anything under `case:` or `project:`
   must stay identical, or the two files become different pages
4. Run `make check` and confirm the language's coverage went up

---

## Coverage thresholds

`scripts/translation-status.py` enforces a minimum per language:

```python
LANGUAGES = {
    "en": 1.00,   # default language, must be complete
    "nl": 1.00,   # ANBI content is inherently Dutch, so this is enforced
    "de": 0.00,   # tracked, not yet enforced
    "fr": 0.00,
    "es": 0.00,
}
```

German, French and Spanish are at `0.00` because they have interface strings but no translated page
content yet. They are still counted and listed on every run, so the gap stays visible.

**Raise a threshold as soon as a language has a named reviewer.** Leaving them at zero forever is how
this turns into scaffolding.

---

## Stale translations

The script also flags translations older than their English source, using git commit times. That
catches the common case: someone edits the English page and the other four quietly fall behind.
Stale pages count as failures for any language at 100%.

---

## Machine translation

Acceptable as a first pass. Not acceptable as the last step.

Every language needs a named person who reads it to review before it goes live, particularly for the
Code of Conduct and case write-ups, where wording carries legal and technical weight. Get the
reviewer first, then translate.
