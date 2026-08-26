---
untranslated: true
title: "CG-2024-00001 JetBrains TeamCity authenticatie-omzeiling"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Summary

A significant security vulnerability has been recently uncovered in TeamCity On-Premises. In the
event of exploitation, this flaw has the potential to empower an unauthorized attacker, who has
HTTP(S) access to a TeamCity server, to bypass authentication checks successfully. Consequently, such
an attacker could acquire **administrative** control over the affected TeamCity server, posing a
serious risk to the integrity and security of the system. It is imperative to address and remediate
this issue promptly to safeguard the confidentiality and proper functioning of the TeamCity
On-Premises environment.

### Update

JetBrains recommends that On-Prem users promptly update to the most recent version (2023.11.3) or,
alternatively, apply the provided security patch to prevent unauthorised access. See their
[blog](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)
for more details.

### Compromise Assessment

Where possible, you should also conduct a compromise assessment to check if the exploit has already
been abused by:

- checking access and audit logs and comparing to real human user behaviours (e.g. "Did you really
  login in at Midnight Dave?")
- checking for signs of persistence such as new user accounts (e.g. "Who is Elaine.Ransom?")

This includes the TeamCity server itself as well as any other servers that can be accessed from it
such as CI/CD assets.
