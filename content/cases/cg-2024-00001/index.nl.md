---
title: "JetBrains TeamCity authenticatie-omzeiling"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Samenvatting

Er is onlangs een ernstige beveiligingskwetsbaarheid ontdekt in TeamCity On-Premises. Bij misbruik
stelt dit lek een aanvaller zonder toegangsrechten, die wel HTTP(S)-toegang heeft tot een
TeamCity-server, in staat om de authenticatiecontroles te omzeilen. Zo'n aanvaller kan daardoor
**beheerdersrechten** krijgen over de betreffende TeamCity-server, wat een serieus risico vormt voor
de integriteit en de veiligheid van het systeem. Het is noodzakelijk dit probleem snel te verhelpen
om de vertrouwelijkheid en de goede werking van de TeamCity On-Premises-omgeving te waarborgen.

### Update

JetBrains raadt On-Prem-gebruikers aan direct bij te werken naar de nieuwste versie (2023.11.3) of
anders de meegeleverde beveiligingspatch toe te passen om ongeautoriseerde toegang te voorkomen. Zie
hun
[blog](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)
voor meer details.

### Onderzoek naar misbruik

Voer waar mogelijk ook een onderzoek uit om vast te stellen of het lek al is misbruikt, door:

- toegangs- en auditlogs te controleren en te vergelijken met echt menselijk gedrag (bijvoorbeeld:
  "Heb je om middernacht echt ingelogd, Dave?")
- te letten op sporen van persistentie, zoals nieuwe gebruikersaccounts (bijvoorbeeld: "Wie is
  Elaine.Ransom?")

Dit geldt voor de TeamCity-server zelf en voor alle andere servers die vanaf die server bereikbaar
zijn, zoals CI/CD-systemen.
