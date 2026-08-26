---
title: "Hope: credenciales expuestas en buckets públicos"
slug: "CG-2024-00003"
date: 2024-04-15T09:00:00+02:00
lastmod: 2024-04-19T00:00:00+02:00
---

### Resumen

Los buckets públicos están expuestos a todo el mundo. Aunque resultan útiles para sitios web o
conjuntos de datos públicos, es poco probable que alguien deposite credenciales en ellos a propósito.
En este caso escaneamos un gran número de buckets expuestos públicamente en proveedores como:

- AWS S3
- Azure Blob Storage
- Google Cloud Platform Buckets

en busca de credenciales del tipo:

- tokens de acceso de AWS
- tokens OAuth
- claves de API
- cuentas de servicio de GCP

### Medidas a tomar

- Retirar del bucket las credenciales expuestas
- Rotar las credenciales expuestas
- Determinar si el resto del contenido del bucket debe ser público y restringir el acceso según
  corresponda
- Analizar los registros para determinar si las credenciales expuestas se han usado indebidamente
- Deshacer las acciones indebidas

En algunos tipos de credenciales, sobre todo los accesos a proveedores de nube, el riesgo de abuso es
alto y puede derivar en movimiento lateral y escalada de privilegios. Amazon publica guías detalladas
para estas situaciones:

- [Public Access to S3](https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/S3_Public_Access.md)
- [Incident Response: Data Access](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-DataAccess.md)
- [Incident Response: Compromised Credentials](https://github.com/aws-samples/aws-incident-response-playbooks/blob/master/playbooks/IRP-CredCompromise.md)
