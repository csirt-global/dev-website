---
title: "You received an email from us"
description: "CSIRT.global contacted you about a vulnerability in a system you own. Here is how to check the email is genuine, what we did and did not do, and what to do next."
layout: "notified"
---

We found a security problem affecting a system registered to your organisation, and we contacted you
about it. This page explains who we are, how to check that the message is genuine, and what to do
next.

**We will never ask you for payment, credentials, or access to your systems.** If a message claiming
to be from us asks for any of those, it is not from us.

## How to check the email is genuine

Our notifications come from an address ending in **`@csirt.global`**. That may be
`inquiries@csirt.global`, a case address such as `CG-2024-00001@csirt.global`, or the personal
CSIRT.global address of the researcher handling the case.

Check the sender domain carefully. Look for lookalike spellings such as `csirt-global.com` or
`cslrt.global`. If the domain is not exactly `csirt.global`, treat it as suspicious.

Every case we open is published in our [case register](/cases/), with the date, the vulnerability and
the researchers involved. If our email references a case number, you can look it up there.

You can also contact us directly, using an address you found here rather than one from the email:
[inquiries@csirt.global](mailto:inquiries@csirt.global).

## What we did

We scan the public internet for systems affected by known vulnerabilities, and for credentials that
have been exposed in publicly reachable locations. When we find one, we identify the owner and get in
touch.

We did **not** access your data, exploit the vulnerability, or make any change to your systems. Where
we needed to confirm a finding, we did so with the minimum interaction necessary, using
non-weaponised checks. Our [Code of Conduct](/about/code-of-conduct/) sets out the limits we work
within, and we are bound by them.

We do this because unreported vulnerabilities get found eventually, usually by someone with worse
intentions. We are a volunteer-led not-for-profit foundation. Nobody pays us to contact you, and we
are not selling anything.

## What to do next

1. **Verify the sender**, using the checks above.
2. **Read the finding.** The email describes the affected host and the specific issue.
3. **Fix or mitigate it.** Where a patch or workaround exists, we include it.
4. **Reply if you need to.** If something is unclear, if you are not the right owner, or if you would
   like help, tell us. A reply also confirms the message reached the right person.

Remediation is your responsibility, and it stays under your control. We report; we do not intervene.

## If you would like us to keep looking

Some organisations ask us to scan them regularly, rather than waiting for us to find something.
Charities and NGOs can also be nominated for a fully funded
[bug bounty programme](/what-we-do/bug-bounties/). Both are free.
