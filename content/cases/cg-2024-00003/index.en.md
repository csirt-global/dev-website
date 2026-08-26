---
title: "Hope: Exposed Credentials in Public Buckets"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
case:
  id: "CG-2024-00003"
  ref: "CG-2024-00003 Hope: Exposed Credentials in Public Buckets"
  status: current
  lead: "Soufian El Yadmani"
  leadAnchor: soufian
  researchers: ["Gabriel Tarsia", "Michael Rowley", "Sophia Guarnotta", "Tyler Kay"]
  cwe:
    - { id: "CWE-538", label: "CWE-538: Insertion of Sensitive Information into Externally-Accessible File or Directory", url: "https://cwe.mitre.org/data/definitions/538.html" }
    - { id: "CWE-522", label: "CWE-522: Insufficiently Protected Credentials", url: "https://cwe.mitre.org/data/definitions/522.html" }
---

### Summary

Public Buckets are exposed to the world at large. While they can be useful for things like websites
and public data stores, it is unlikely that credentials will be intentionally placed here. During
this case, we scanned large numbers of publicly exposed buckets from providers like:

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

for credentials like:

- AWS Access Tokens
- OAuth Tokens
- API keys
- GCP Service Accounts

### Response Actions

- Remove the publicly exposed credentials from the bucket
- Rotate the publicly exposed credentials
- Determine if the other bucket contents should be public and restrict access appropriately
- Analyse logs to determine if the exposed credential was abused
- Undo abusive actions

For some credential types (notably cloud provider access), the potential for abuse is high and can
lead to further lateral movement and privilege escalation. Amazon have provided some detailed
playbooks to tackle these situations:

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
