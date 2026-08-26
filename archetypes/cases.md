---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
# The slug is the case identifier and its URL is externally citable.
# Keep the capitals: GitHub Pages is case-sensitive.
slug: "CG-{{ now.Year }}-00000"
date: {{ .Date }}
case:
  id: "CG-{{ now.Year }}-00000"
  ref: ""
  status: current          # current | closed
  lead: ""
  leadAnchor: ""           # anchor of the lead on /about/team/
  researchers: []
  cve: []
  product: ""
  productUrl: ""
---

What the vulnerability is, who is affected, and what owners should do.
