---
title: "JetBrains TeamCity Authentifizierungs-Umgehung"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Zusammenfassung

In TeamCity On-Premises wurde kürzlich eine schwerwiegende Sicherheitslücke entdeckt. Wird sie
ausgenutzt, ermöglicht sie einer nicht berechtigten angreifenden Person mit HTTP(S)-Zugriff auf einen
TeamCity-Server, die Authentifizierungsprüfungen zu umgehen. Dadurch kann sie **administrative**
Kontrolle über den betroffenen TeamCity-Server erlangen, was Integrität und Sicherheit des Systems
ernsthaft gefährdet. Das Problem muss zügig behoben werden, um die Vertraulichkeit und den
ordnungsgemäßen Betrieb der TeamCity-On-Premises-Umgebung zu sichern.

### Update

JetBrains empfiehlt On-Prem-Nutzenden, umgehend auf die neueste Version (2023.11.3) zu aktualisieren
oder andernfalls den bereitgestellten Sicherheitspatch einzuspielen, um unbefugten Zugriff zu
verhindern. Näheres im
[Blog](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)
von JetBrains.

### Prüfung auf Kompromittierung

Prüft nach Möglichkeit auch, ob die Lücke bereits ausgenutzt wurde:

- Zugriffs- und Auditprotokolle prüfen und mit tatsächlichem menschlichem Verhalten abgleichen (etwa:
  "Hast du dich wirklich um Mitternacht angemeldet, Dave?")
- auf Spuren von Persistenz achten, etwa neue Benutzerkonten (etwa: "Wer ist Elaine.Ransom?")

Das gilt für den TeamCity-Server selbst wie für alle anderen Server, die von ihm aus erreichbar sind,
etwa CI/CD-Systeme.
