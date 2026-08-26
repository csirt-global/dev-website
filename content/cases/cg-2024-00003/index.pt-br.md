---
title: "Hope: credenciais expostas em buckets públicos"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
---

### Resumo

Buckets públicos ficam expostos ao mundo inteiro. Eles são úteis para coisas como sites e repositórios
de dados abertos, mas é pouco provável que alguém queira colocar credenciais ali de propósito. Neste
caso, varremos um grande número de buckets expostos publicamente em provedores como:

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

à procura de credenciais como:

- tokens de acesso da AWS
- tokens OAuth
- chaves de API
- contas de serviço do GCP

### Ações de resposta

- Remova do bucket as credenciais expostas publicamente
- Troque as credenciais expostas publicamente
- Avalie se o restante do conteúdo do bucket deve mesmo ser público e restrinja o acesso conforme o caso
- Analise os registros para descobrir se a credencial exposta foi usada indevidamente
- Desfaça as ações indevidas

Para alguns tipos de credencial, sobretudo as de acesso a provedores de nuvem, o potencial de abuso é
alto e pode levar a movimentação lateral e escalonamento de privilégios. A Amazon publicou manuais
detalhados para lidar com essas situações:

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
