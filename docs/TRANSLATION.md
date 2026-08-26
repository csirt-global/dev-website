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

## Changing one language changes all of them

If a pull request edits a page in one language, it edits that page in every language it exists in.
`scripts/check-translation-sync.py` enforces it, and a correction to a case record is a correction in
seven files.

It reads the **diff**, not the state of the repository. Comparing file timestamps was the obvious
approach and does not work: every language here was written in its own pull request, so timestamps
say Spanish is the newest version of every page on the site. True, and useless.

Adding a translation is not editing one, so a new file never triggers it. That is how a language gets
written in the first place.

When a change genuinely does not apply elsewhere, write the reason in the commit message rather than
making six no-op edits:

```
Translation-sync: not-required, fixes a Dutch-only typo
```

## Coverage thresholds

A threshold is per language and says one thing: **this language is complete, keep it that way.**

The five configured today are all at 100%, so all five are enforced. Adding an English page without
its translations fails the build, which is what stops the gap reopening one page at a time.

A language still being written sits at `0.00` and is only reported. That is how English, and then
each of the other four, got here. **Raising a threshold is the last step of adding a language, not a
precondition for starting one**, so a new language does not fail CI on the day it is configured.

If a single page genuinely cannot be translated yet in a finished language, add the file with
`untranslated: true` rather than lowering that language's threshold. It renders with a notice telling
readers why they are seeing English, and it counts as missing until it is real.



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

## Reviewed, or not

Every translation here was written without a native speaker to check it, and that is tracked but not
announced.

A reviewer who has read a page adds one line to its front matter:

```yaml
reviewed: true
```

`translation-status.py` counts unreviewed pages per language, so the gap is visible to anyone working
on the site. It blocks nothing.

**There is deliberately no notice on the page itself.** A volunteer organisation will not sustain a
native speaker signing off every page in five languages, so that notice would be permanent, and a
permanent warning on every non-English page tells the one audience deciding whether to trust us that
we are not sure about our own site. The cure was worse than the disease.

What is announced is the honest, temporary case: a page that has not been translated at all says so,
because the reader is looking at English and deserves to know why.

## Linking to the English version on purpose

`layouts/partials/href.html` rewrites every internal Markdown link to the current language, which is
right for navigation and wrong when you mean the English page specifically. A Markdown link to
`/about/code-of-conduct/` on the Dutch page resolves back to the Dutch page.

Raw HTML skips the render hook, so this works:

```html
<a href="/about/code-of-conduct/">Engelse tekst</a>
```

The Code of Conduct uses it for the line stating that the English text governs. The language
switcher covers the ordinary case, so this is rarely needed.

## English left inside a translated file

`untranslated: true` is a manual flag, so it only catches the honest mistake. `translation-status.py`
also compares each translated body against its English source and fails the language when a body is
85% or more the same words.

Identifiers, URLs, code spans and numbers are stripped before comparing, because those are supposed
to be identical in every language. For calibration: a file copied straight from English scores 100%,
while the genuine Dutch translations score between 0% and 23%, the highest being case pages, which
share technical vocabulary with their source.

## Machine translation

Acceptable as a first pass. Not acceptable as the last step.

Every language needs a named person who reads it to review before it goes live, particularly for the
Code of Conduct and case write-ups, where wording carries legal and technical weight. Get the
reviewer first, then translate.
