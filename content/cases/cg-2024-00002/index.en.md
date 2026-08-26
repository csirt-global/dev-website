---
title: "Connectwise ScreenConnect Authentication Bypass"
slug: "CG-2024-00002"
date: 2024-02-21T13:00:00+01:00
lastmod: 2024-02-26T22:41:00+01:00
case:
  id: "CG-2024-00002"
  ref: "CG-2024-00002-Connectwise-Screenconnect"
  status: closed
  lead: "Soufian El Yadmani"
  leadAnchor: soufian
  researchers: ["Chris Heald", "Gabriel Tarsia", "Michael Rowley", "Soufian El Yadmani", "Tuhin Mukherjee", "Victor Gevers", "Brad Lynch"]
  cve: ["CVE-2024-1708", "CVE-2024-1709"]
  product: "ScreenConnect"
  productUrl: "https://screenconnect.connectwise.com/support/live-demo"
  vulnerableVersions: "ScreenConnect 23.9.7 and prior"
  vendorStatement: "https://www.connectwise.com/company/trust/security-bulletins/connectwise-screenconnect-23.9.8"
---

### Summary

ConnectWise addressed ScreenConnect vulnerabilities enabling unauthorized administrator account
creation, with a published exploit of trivial difficulty significantly elevating the risk. This
exploit is being used by Ransomware crews. Immediate update to version 23.9.8 is required for
self-hosted/on-premise users. Confirmed compromised accounts and associated threat actor IP
addresses are shared on the ConnectWise website.

### Other Resources

- [A catastrophe for control: understanding the ScreenConnect authentication bypass](https://www.huntress.com/blog/a-catastrophe-for-control-understanding-the-screenconnect-authentication-bypass)
