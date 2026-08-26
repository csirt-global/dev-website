---
title: "Elusión de autenticación en JetBrains TeamCity"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Resumen

Se ha descubierto recientemente una vulnerabilidad de seguridad importante en TeamCity On-Premises.
Si se explota, esta falla permite a una persona no autorizada con acceso HTTP(S) a un servidor
TeamCity eludir los controles de autenticación. Así puede obtener control **administrativo** sobre el
servidor TeamCity afectado, lo que supone un riesgo serio para la integridad y la seguridad del
sistema. Es imprescindible resolver el problema con rapidez para preservar la confidencialidad y el
funcionamiento correcto del entorno TeamCity On-Premises.

### Actualización

JetBrains recomienda a quienes usan On-Prem actualizar sin demora a la última versión (2023.11.3) o,
en su defecto, aplicar el parche de seguridad facilitado para impedir accesos no autorizados. Más
detalles en su
[blog](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/).

### Comprobación de compromiso

Siempre que sea posible, comprobad también si la falla ya se ha aprovechado:

- revisando los registros de acceso y auditoría y comparándolos con el comportamiento humano real
  (por ejemplo: «¿De verdad entraste a medianoche, Dave?»)
- buscando señales de persistencia, como cuentas de usuario nuevas (por ejemplo: «¿Quién es
  Elaine.Ransom?»)

Esto incluye tanto el propio servidor TeamCity como cualquier otro servidor accesible desde él, por
ejemplo los sistemas de CI/CD.
