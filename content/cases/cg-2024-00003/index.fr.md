---
title: "Hope : identifiants exposés dans des buckets publics"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
---

### Résumé

Les buckets publics sont accessibles à tous. S'ils sont utiles pour des sites web ou des jeux de
données publics, il est peu probable que des identifiants y soient déposés intentionnellement. Dans
ce cas, nous avons scanné un grand nombre de buckets exposés publiquement chez des fournisseurs tels
que :

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

à la recherche d'identifiants du type :

- jetons d'accès AWS
- jetons OAuth
- clés d'API
- comptes de service GCP

### Mesures à prendre

- Retirer du bucket les identifiants exposés
- Renouveler les identifiants exposés
- Déterminer si le reste du contenu du bucket doit être public et restreindre l'accès en conséquence
- Analyser les journaux pour déterminer si l'identifiant exposé a été utilisé abusivement
- Annuler les actions abusives

Pour certains types d'identifiants, notamment les accès aux fournisseurs cloud, le risque d'abus est
élevé et peut mener à une propagation latérale et à une élévation de privilèges. Amazon met à
disposition des guides détaillés pour ces situations :

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
