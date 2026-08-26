---
title: "Hope: blootgestelde inloggegevens in publieke buckets"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
# Only the fields whose wording is language-dependent. Everything else
# comes from data/cases/CG-2024-00003.yaml.
case:
  ref: "CG-2024-00003 Hope: blootgestelde inloggegevens in publieke buckets"
---

### Samenvatting

Publieke buckets zijn voor iedereen toegankelijk. Dat is nuttig voor bijvoorbeeld websites en open
datasets, maar het is onwaarschijnlijk dat inloggegevens daar bewust worden neergezet. In deze case
hebben wij grote aantallen publiek toegankelijke buckets gescand bij aanbieders als:

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

op inloggegevens zoals:

- AWS-toegangstokens
- OAuth-tokens
- API-sleutels
- GCP-serviceaccounts

### Aanbevolen maatregelen

- Verwijder de publiek toegankelijke inloggegevens uit de bucket
- Roteer de blootgestelde inloggegevens
- Bepaal of de overige inhoud van de bucket publiek hoort te zijn en beperk de toegang waar nodig
- Analyseer logbestanden om vast te stellen of de gegevens zijn misbruikt
- Draai misbruik terug

Bij sommige soorten inloggegevens, met name toegang tot cloudomgevingen, is de kans op misbruik groot
en kan dit leiden tot verdere laterale beweging en rechtenescalatie. Amazon biedt uitgebreide
draaiboeken voor deze situaties:

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
