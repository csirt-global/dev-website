---
title: "Contournement d'authentification JetBrains TeamCity"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Résumé

Une vulnérabilité de sécurité importante a récemment été découverte dans TeamCity On-Premises. Si
elle est exploitée, cette faille permet à une personne non autorisée disposant d'un accès HTTP(S) à
un serveur TeamCity de contourner les contrôles d'authentification. Elle peut ainsi obtenir un
contrôle **administrateur** sur le serveur TeamCity concerné, ce qui met sérieusement en danger
l'intégrité et la sécurité du système. Il est impératif de corriger ce problème rapidement afin de
préserver la confidentialité et le bon fonctionnement de l'environnement TeamCity On-Premises.

### Mise à jour

JetBrains recommande aux utilisateurs On-Prem de passer sans tarder à la dernière version (2023.11.3)
ou, à défaut, d'appliquer le correctif de sécurité fourni afin d'empêcher tout accès non autorisé.
Voir leur
[blog](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)
pour plus de détails.

### Recherche de compromission

Dans la mesure du possible, vérifiez également si la faille a déjà été exploitée :

- en examinant les journaux d'accès et d'audit et en les comparant au comportement humain réel (par
  exemple : « Tu t'es vraiment connecté à minuit, Dave ? »)
- en cherchant des traces de persistance, comme de nouveaux comptes utilisateurs (par exemple :
  « Qui est Elaine.Ransom ? »)

Cela vaut pour le serveur TeamCity lui-même comme pour tout autre serveur accessible depuis
celui-ci, notamment les systèmes CI/CD.
