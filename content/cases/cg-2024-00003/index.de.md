---
title: "Hope: Offengelegte Zugangsdaten in öffentlichen Buckets"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
---

### Zusammenfassung

Öffentliche Buckets sind für alle zugänglich. Für Websites und öffentliche Datenbestände können sie
sinnvoll sein, aber Zugangsdaten landen dort kaum mit Absicht. In diesem Fall haben wir eine große
Zahl öffentlich zugänglicher Buckets bei Anbietern wie:

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

auf Zugangsdaten dieser Art untersucht:

- AWS Access Tokens
- OAuth Tokens
- API-Schlüssel
- GCP Service Accounts

### Maßnahmen

- Die offengelegten Zugangsdaten aus dem Bucket entfernen
- Die offengelegten Zugangsdaten austauschen
- Prüfen, ob die übrigen Inhalte des Buckets öffentlich sein sollen, und den Zugriff entsprechend
  einschränken
- Protokolle auswerten, um festzustellen, ob die offengelegten Zugangsdaten missbraucht wurden
- Missbräuchliche Handlungen rückgängig machen

Bei manchen Arten von Zugangsdaten, insbesondere Zugängen zu Cloud-Anbietern, ist das Missbrauchsrisiko
hoch und kann zu weiterer Ausbreitung im Netz und zu Rechteausweitung führen. Amazon stellt dazu
ausführliche Handlungsanleitungen bereit:

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
