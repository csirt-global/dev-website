# Reproducible builds: both tools are pinned, neither needs npm.
HUGO_VERSION := $(shell cat .hugo_version)
TAILWIND_VERSION := 4.3.3
TAILWIND := bin/tailwindcss

.PHONY: all css build serve check sweep clean tools

all: check

tools: $(TAILWIND)
$(TAILWIND):
	@mkdir -p bin
	curl -sL -o $@ https://github.com/tailwindlabs/tailwindcss/releases/download/v$(TAILWIND_VERSION)/tailwindcss-macos-arm64
	chmod +x $@

css: $(TAILWIND)
	$(TAILWIND) -i assets/css/main.css -o assets/css/build.css --minify

# public/ is removed first: fingerprinted filenames change on every CSS edit,
# so an incremental build leaves orphaned stylesheets behind.
build: css
	rm -rf public
	hugo --gc --minify

serve: css
	hugo server --bind 0.0.0.0 --port 1313

# Everything except translation-status reads ./public, so check builds first.
check: build
	python3 scripts/translation-status.py
	python3 scripts/check-urls.py
	python3 scripts/check-links.py
	python3 scripts/check-translation-sync.py
	python3 scripts/check-css.py
	python3 scripts/check-security-txt.py
	python3 scripts/check-donate.py
	python3 scripts/check-content-parity.py

# Browser sweep. Needs `make serve` running in another terminal, and Playwright
# (`npm ci`) — the only npm dependency, and no part of the site build.
sweep:
	node scripts/sweep.mjs

clean:
	rm -rf public resources assets/css/build.css
