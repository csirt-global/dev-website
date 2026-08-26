# Security policy

CSIRT.global finds and reports vulnerabilities in other people's systems. It
would be a poor look to be difficult about our own, so this is deliberately
short.

## Reporting a vulnerability in this website

Report it through our Coordinated Vulnerability Disclosure form:

**https://app.zerocopter.com/en/cvd/8b2fbf09-539f-4b09-bee0-2ec875cb3321**

Or email **inquiries@csirt.global** if that is easier. The same addresses are
published in [`/.well-known/security.txt`](static/.well-known/security.txt) per
RFC 9116, and `scripts/check-security-txt.py` fails the build thirty days before
that file expires so it cannot quietly lapse.

Please give us a reasonable window to fix something before publishing it. We
will tell you what we found, what we changed, and when.

## What this repository is

A static site. It is built by Hugo into plain HTML and served by GitHub Pages.
There is no server, no database, no user accounts and no form on our own
infrastructure, so the realistic attack surface is:

- **The build**: a malicious pull request, or a compromised GitHub Action.
  Workflow permissions are `contents: read`, both tool versions are pinned, and
  the deploy workflow builds from `main` only.
- **Third-party embeds**: the volunteer form is JotForm, the news feed is
  Supascribe, analytics is GoatCounter, and Alpine.js is loaded from a CDN
  pinned to an exact version with a subresource integrity hash. A compromise of
  any of those is a compromise of the page they appear on. They are listed in
  [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) with that in mind.
- **The published documents**: the ANBI filings under `/uploads/` are statutory
  publications. Their URLs must not change and their contents must not be
  edited outside a pull request.

## What is out of scope

Findings that need no action from us, because there is nothing to protect:

- Missing security headers that a static host cannot set
- Absent rate limiting, CSRF tokens, or session handling on a site with no
  sessions
- Automated scanner output with no demonstrated impact
- Reports about the third-party services above; take those to their own
  disclosure programmes

## Our own conduct

How we behave when we are the ones doing the reporting is set out in our
[Code of Conduct](https://csirt.global/about/code-of-conduct/). We hold
ourselves to it, and you are welcome to hold us to it too.
