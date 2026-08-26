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

### Reporter evidence beats reasoning

Three issues in this repo were diagnosed from their titles, and two of the three
conclusions reversed once the attached screenshots were actually opened. Open
the image.
