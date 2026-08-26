---
# The vulnerability in plain words. No CVE and no case id: both render as their
# own fields, so repeating them here duplicates them on every row of /cases/.
title: ""
# The public URL, externally cited and case-sensitive. Taken from the folder
# name, so the folder decides it. Keep the capitals.
slug: "{{ .File.ContentBaseName }}"
date: {{ .Date }}
#
# The facts do NOT go here. Status, lead, researchers, CVEs, product, versions
# and the vendor statement are identical in every language, so they live once in
#
#     data/cases/{{ .File.ContentBaseName }}.yaml
#
# and the build fails with a message naming that file until it exists. Copy an
# existing one and edit it.
#
# A translation may add a `case:` block of its own to override a single field
# that genuinely carries prose, such as a version range ending in "and prior".
---

What the vulnerability is, who is affected, and what owners should do.
