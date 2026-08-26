---
title: "Connectwise - ScreenConnect authenticatie-omzeiling"
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
  vulnerableVersions: "ScreenConnect 23.9.7 en ouder"
  vendorStatement: "https://www.connectwise.com/company/trust/security-bulletins/connectwise-screenconnect-23.9.8"
---

### Samenvatting

ConnectWise heeft kwetsbaarheden in ScreenConnect verholpen waarmee ongeautoriseerd
beheerdersaccounts konden worden aangemaakt. Er is een exploit gepubliceerd die eenvoudig te
gebruiken is, wat het risico aanzienlijk vergroot. Deze exploit wordt ingezet door ransomwaregroepen.
Voor gebruikers met een eigen installatie is direct bijwerken naar versie 23.9.8 noodzakelijk.
Bevestigde gecompromitteerde accounts en bijbehorende IP-adressen van aanvallers worden gedeeld op de
website van ConnectWise.

### Overige bronnen

- [A catastrophe for control: understanding the ScreenConnect authentication bypass](https://www.huntress.com/blog/a-catastrophe-for-control-understanding-the-screenconnect-authentication-bypass)
