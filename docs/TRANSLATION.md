# Translations

The site ships in seven languages: **English** (default), **Dutch**, **German**, **French**,
**Spanish**, **Brazilian Portuguese** and **Simplified Chinese**.

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

Group names are interface strings, not page content, so they translate once and apply everywhere.
That is why `data/team.yaml` stores `role: role_advisor` rather than `role: "Advisor"`.

Job titles are the exception. They are interface strings too, but they stay in English in every
language: `i18n/en.yaml` is the only file with `role_` keys and the rest fall back to it. Translating
a job title means picking a grammatical gender for a named colleague, which is a guess about a real
person, and the English titles are what those people use elsewhere.

---

## Adding a translation

1. Copy the English file, change the suffix: `index.en.md` → `index.de.md`
2. Translate the body **and** the `title` and `description` in the front matter
3. Leave structural values alone: `slug`, `date`, `weight`, and anything under `case:` or `project:`
   must stay identical, or the two files become different pages
4. Run `make check` and confirm the language's coverage went up

---

## Adding a language

Two languages were added after the original five, and both turned up something the first five never
had to answer. The order below is the one that works.

1. **Declare it in `hugo.yaml`.** The key becomes the URL prefix and stays lowercase, so `pt-br`
   gives `/pt-br/`. Set `label` to the language's own name for itself, and a `weight` for its place
   in the switcher.

2. **Give it a BCP 47 tag if the key is not one.** `params.languageTags` maps the key to the tag the
   markup needs: `pt-br` to `pt-BR`, `zh` to `zh-Hans`. `layouts/partials/lang-tag.html` reads it for
   `<html lang>`, `hreflang` and `og:locale`. A language whose tag equals its key needs no entry.
   `zh` alone does not say whether the script is Simplified or Traditional, which is the whole reason
   this map exists.

   That partial takes the page and reads `.Site` off it. It must never read the global `site`:
   `head.html` calls it inside `range .AllTranslations`, and a partial reading the global would label
   every alternate link with the language of the page being rendered instead of the one it points at.

3. **Shorten the switcher chip if the key is long.** `params.languageCodes` overrides it, which is
   why Brazilian Portuguese shows `BR` rather than `PT-BR`.

4. **Add it to `LANGS` in `scripts/sweep.mjs`.** This measures whether the header still fits. French
   needed 1,103px of the 1,088 available before its labels were shortened, and nobody noticed until a
   screenshot arrived. Do this before writing a word, not after.

5. **Add it to `LANGUAGES` in `scripts/translation-status.py` at `0.00`.** Now the gap is counted and
   listed while you work, and nothing is blocked.

6. **Write the 22 pages and the interface strings.** `i18n/<lang>.yaml` needs every key in
   `i18n/en.yaml` except the `role_` keys, which stay English everywhere. Include `date_long`.

7. **Raise the threshold to `1.00`** in the same pull request. That is the last step.

### `date_long`

Dates are written with a Go time layout held as an i18n key, because month names are not the only
thing that differs:

```yaml
en:    date_long: "2 January 2006"        ->  16 February 2024
de:    date_long: "2. January 2006"       ->  16. Februar 2024
es:    date_long: "2 de January de 2006"  ->  16 de febrero de 2024
zh:    date_long: "2006年1月2日"           ->  2024年2月16日
```

`January` and `2006` are reference tokens Go substitutes; everything else is passed through
literally, which is the room the connectors need. Use `time.Format`, never `.Date.Format`: the
latter hardcodes English month names whatever the site language is.

### A script the site has not set before

Chinese was the first non-Latin script here, and it needed exactly two things beyond the list above,
both already in place for the next one:

- **No webfont.** Our three faces are Latin-only. Chinese falls through `ui-sans-serif` to the
  reader's own CJK font. See [ARCHITECTURE.md](ARCHITECTURE.md).
- **`:lang(zh)` turns off the Latin display tracking** in `assets/css/main.css`, because Han glyphs
  sit on a fixed square body and tracking them apart reads as damage. It deliberately leaves
  `text-transform` alone: uppercasing is a no-op on a script with no case, so overriding it changes
  nothing for Han and only un-uppercases the Latin strings that remain on the page.

---

## Changing one language changes all of them

If a pull request edits a page in one language, it edits that page in every language it exists in.
`scripts/check-translation-sync.py` enforces it, and a correction to a page is a correction in seven
files. Case *facts* are the deliberate exception: they live once in `data/cases/`, so correcting a
CVE is one edit, not seven.

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

`scripts/translation-status.py` holds a minimum per language. A threshold says one thing: **this
language is complete, keep it that way.**

```python
LANGUAGES = {
    "en": 1.00,
    "nl": 1.00,
    "de": 1.00,
    "fr": 1.00,
    "es": 1.00,
    "pt-br": 1.00,
    "zh": 1.00,
}
```

All seven are at 100%, so all seven are enforced. Adding an English page without its translations
fails the build, which is what stops the gap reopening one page at a time.

A language still being written sits at `0.00` and is only reported. That is how each of these got
here. **Raising a threshold is the last step of adding a language, not a precondition for starting
one**, so a new language does not fail CI on the day it is configured, and there is no window in
which a half-written language blocks everyone else's work.

A threshold is not a claim that a language has been reviewed. Nothing here has a named reviewer, and
withholding the threshold until one exists would mean withholding it forever. See *Reviewed, or not*
below.

If a single page genuinely cannot be translated yet in a finished language, add the file with
`untranslated: true` rather than lowering that language's threshold. It renders with a notice telling
readers why they are seeing English, and it counts as missing until it is real.

---

## Stale translations

The script also flags translations older than their English source, using git commit times. That
catches the common case: someone edits the English page and the other six quietly fall behind.
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
native speaker signing off every page in seven languages, so that notice would be permanent, and a
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
one where only the headings were translated scores 93%, and the genuine translations score between
0% and 23%, the highest being case pages, which share technical vocabulary with their source.

**Han counts as words.** The comparison splits on a character class containing no Han, so a Chinese
body yielded no tokens at all and the only ones left were its Latin identifiers, which are meant to
be identical in every language. A correct translation scored 100% and failed the build. Each
ideograph is now its own token. A future language written in another script without spaces needs the
same treatment.

## Machine translation

Acceptable as a first pass. Not acceptable as the last step.

Every language needs a named person who reads it to review before it goes live, particularly for the
Code of Conduct and case write-ups, where wording carries legal and technical weight. Get the
reviewer first, then translate.

That is the standard, and this repository does not meet it: seven languages are published and none
has been read by a native speaker. It is tracked by the `reviewed:` flag rather than hidden, and it
is the largest outstanding item on the translations.
