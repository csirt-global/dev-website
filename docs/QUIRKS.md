# Quirks

Things that have gone wrong in this repository, and how they are prevented from
going wrong again. Read this before editing templates or CSS.

Every entry is something that actually happened here, not a general warning.

---

## Hugo

### `.` inside `range` is the item, not the page

```go-html-template
{{ range .Params.project.team }}
  {{ .name }}                      {{/* the team member */}}
  {{ $.Params.project.name }}      {{/* the page — $ is the page, not . */}}
{{ end }}
```

This bit three separate templates: `team.html`, `projects/single.html` and
`cases/list.html`. In each case `.name` inside a `range` silently rendered
nothing, because the page has no `name`. The fix is to capture the item first:

```go-html-template
{{ range .members }}{{ $m := . }}
  <img alt="{{ $m.name }}">
{{ end }}
```

### A partial reading global `site` ignores the item it was given

The same trap as `.` inside `range`, one level further out. `layouts/partials/head.html` builds the
alternate-language links like this:

```go-html-template
{{- range .AllTranslations }}
<link rel="alternate" hreflang="{{ partial "lang-tag.html" . }}" href="{{ .Permalink }}">
{{- end }}
```

The partial was written as `{{ return ... site.Language.Lang }}`. `site` is the *current* site,
regardless of what the partial was handed, so every alternate link on every page carried the
language of the page being rendered: `/pt-br/` advertised all six alternates as `hreflang="pt-BR"`.

Inside a partial, read `.Site`, never `site`. The first follows the argument, the second does not.

### Aliases are prefixed with the page's language

```yaml
aliases: ["/es/donate/"]      # on content/get-involved/donate/index.es.md
```

publishes `/es/es/donate/`, and leaves `/es/donate/` a 404. Hugo prefixes an alias with the language
of the page carrying it, so the alias is written **unprefixed** and the prefix is added for you:

```yaml
aliases: ["/donate/"]         # publishes /es/donate/ on the Spanish page
```

This shipped in four languages and nothing caught it. `check-urls.py` only lists URLs someone
thought to add.

### `cond` evaluates both branches

`cond` is a function, not a conditional. Both arguments are evaluated before it
returns, so this fails the build when the image is an SVG:

```go-html-template
{{ $img := cond (eq .MediaType.SubType "svg") . (.Resize "400x webp") }}
```

Use a real `if`/`else`. `.Resize` on an SVG is an error, and it runs regardless.

### Render hooks emit their own whitespace

A render hook's template whitespace goes into the page verbatim. One untrimmed
newline in `layouts/_default/_markup/render-link.html` put a space in front of
every markdown link on the site: `Vulnerability Disclosure ( DIVD)`, `case
register , with the date`.

Trim every action (`{{- … -}}`), trim comments too (`{{- /* … */ -}}`), and end
the file without a trailing newline. `check-links.py` fails on whitespace welded
to a link, so this cannot come back quietly.

### `index.md` cannot have child pages

`content/get-involved/index.en.md` is a **leaf bundle**. Anything in a
subdirectory under it is treated as an attached resource, not a page — so the
donate page under it was silently never built. No error, no output.

A section that has children needs `_index.<lang>.md`, a **branch bundle**.

### `where … "!=" true` keeps items that lack the key

Counter-intuitive but useful: `where .Pages "Params.hidden" "!=" true` keeps
every page that does not set `hidden` at all. That is what makes the `hidden`
front-matter flag work without adding it to 40 pages.

### Hugo lowercases URLs by default

`disablePathToLower: true` in `hugo.yaml`. Without it, `/cases/CG-2024-00001/`
becomes `/cases/cg-2024-00001/`, which 404s on GitHub Pages — and looks fine on
macOS, whose filesystem is case-insensitive. `check-urls.py` guards it
explicitly for that reason.

---

## CSS and Tailwind

### The stylesheet must be fingerprinted

It used to be served from a fixed `/css/main.css`, so any browser that had
cached it kept the old one after every change. The symptom is bizarre and easy
to misread: utility classes appear not to exist, chevrons render at their
natural 300×150, and the desktop nav shows below its own breakpoint.

Tailwind writes to `assets/css/build.css` and Hugo fingerprints it, so the
content hash is in the filename. **Never link the stylesheet by a fixed path.**

### Deleting a component class fails silently

Component classes (`.record`, `.status`, `.btn`, `.verify` …) are hand-written
in `assets/css/main.css`. Tailwind generates utilities from the templates, so a
utility cannot go missing — but a component can. A careless edit removed the
whole case-record block and the case register rendered as plain text for three
commits.

`check-css.py` fails when a template uses a component class with no rule.

### `gap-px` over a coloured container paints the empty cells

```html
<ul class="grid gap-px bg-ink-line sm:grid-cols-3">   <!-- don't -->
```

The hairline effect works only while the grid is full. Any group whose item
count is not a multiple of the column count shows the container colour as large
blocks where the missing cells are. Use `gap-4` with a background on each cell.

### Media queries measure the viewport, not the container

The organisation record sits full width on the homepage and in a 26 rem sidebar
on `/notified/`. A `@media (min-width: 40rem)` rule gave the sidebar a 13 rem
label column with 9 rem left for the value, wrapping every URL over four lines.

It uses `container-type: inline-size` and `@container` now. Any component that
appears at two different widths should.

### `word-break: break-all` breaks meaning

It split `csirt-global.com` as `csi / rt-global.com` — on the page whose entire
point is telling people to look closely at the sender domain. Use
`overflow-wrap: anywhere`, which only breaks when a token genuinely cannot fit.

### `x-cloak` needs a rule you have to write yourself

```css
[x-cloak] { display: none !important; }
```

Without it, everything Alpine hides with `x-show` is visible until Alpine
initialises. The mobile menu is `fixed inset-0`, so it painted over the whole
page on first load.

### Specificity: prose rules beat utility classes

`.prose-body a` (0,1,1) beats a `text-muted` class (0,1,0) on the same element.
Social icons inside prose came out yellow for that reason. Scope prose rules to
direct children (`[&>li>a]`) or raise the specificity of the exception.

---

## Third-party embeds

### JotForm cannot be styled from here

It is a cross-origin iframe. Its colours live in the JotForm account, not in
this repository. What we do control is the frame: the embed is labelled with who
hosts it, and `/join/` listens for JotForm's `setHeight:<px>` postMessage
(origin-checked) so the whole form is visible without an inner scrollbar.

### Alpine.js is pinned with an integrity hash

The previous site loaded `https://unpkg.com/alpinejs` with no version and no
integrity check, on all eight pages. Whatever the CDN served executed with full
access to the page.

---

## The build

### `public/` must be cleared between builds

Fingerprinted filenames change whenever the CSS does, so an incremental build
accumulates orphaned stylesheets. `make build` removes `public/` first.

### `make build` while `make serve` is running wipes what the server is serving

`make build` starts with `rm -rf public`. If `hugo server` is running in another terminal and has
rendered to disk, the static assets go with it, and the site in the browser comes back with a broken
logo and no favicon. Nothing is actually wrong with the repository.

It cost an hour of looking for a bug in the Chinese stylesheet that did not exist. If you need to
inspect a real build, stop the server first, then serve `public/` with anything static:

```bash
python3 -m http.server 8901 --directory public
```

### The CSS output path is written in one place

`make css`. It used to be repeated in the Makefile and both workflows, and when
it moved, the workflows kept writing to the old path — which would have deployed
the site with no stylesheet at all.

---

## Verification

### Screenshots lie about lazy-loaded images

A full-page screenshot taken immediately after load captures `loading="lazy"`
images below the fold as empty boxes. `scripts/sweep.mjs` scrolls the page
first. A "missing" team photo was this, twice.

### Screenshots lie about transitions

A panel captured mid-transition looks translucent. Wait past the transition
duration before deciding something is a bug — or read the computed style, which
does not lie.

### A check can be blind to a whole script, or a whole string length

Two here have been. `translation-status.py` compared bodies by splitting on a character class with
no Han in it, so a Chinese page yielded no words at all and scored 100% English. `check-content-parity.py`
only inspects text blocks over 30 characters, so it cannot see a person's name being removed.

Neither was wrong about what it measured. Both were silent about something they were assumed to
cover. Before citing a green check as evidence, know what it looks at.

### Reporter evidence beats reasoning

Three issues in this repo were diagnosed from their titles, and two of the three
conclusions reversed once the attached screenshots were actually opened. Open
the image.
