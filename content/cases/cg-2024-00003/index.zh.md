---
title: "Hope：公开存储桶中暴露的凭据"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
---

### 概要

公开存储桶对所有人开放。用来放网站文件或公共数据是合理的，但几乎没有人会有意把凭据放在里面。
在这个案例中，我们扫描了大量对外公开的存储桶，涉及以下服务商：

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

查找的凭据类型包括：

- AWS 访问令牌
- OAuth 令牌
- API 密钥
- GCP 服务账户

### 处置措施

- 把公开暴露的凭据从存储桶中删除
- 轮换这些已暴露的凭据
- 判断存储桶中其余内容是否确实需要公开，并相应收紧访问权限
- 分析日志，确认被暴露的凭据是否已被滥用
- 撤销已经发生的滥用操作

对某些类型的凭据，尤其是云服务商的访问凭据，被滥用的可能性很高，还可能导致横向移动和权限提升。
亚马逊针对这类情况提供了详细的处置手册：

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
