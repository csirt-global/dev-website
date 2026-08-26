---
title: "Contorno de autenticação no JetBrains TeamCity"
slug: "CG-2024-00001"
date: 2024-02-16
---

### Resumo

Foi descoberta recentemente uma vulnerabilidade de segurança grave no TeamCity On-Premises. Se
explorada, a falha permite que uma pessoa não autorizada com acesso HTTP(S) a um servidor TeamCity
contorne as verificações de autenticação. Com isso, ela pode obter controle **administrativo** sobre
o servidor afetado, o que representa risco sério para a integridade e a segurança do sistema. É
essencial corrigir o problema com rapidez para preservar a confidencialidade e o funcionamento
correto do ambiente TeamCity On-Premises.

### Atualização

A JetBrains recomenda que quem usa a versão On-Prem atualize logo para a versão mais recente
(2023.11.3) ou, em alternativa, aplique o patch de segurança disponibilizado, para impedir o acesso
não autorizado. Veja o
[blog da empresa](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)
para mais detalhes.

### Avaliação de comprometimento

Sempre que possível, faça também uma avaliação de comprometimento para verificar se a falha já foi
explorada:

- confira os registros de acesso e de auditoria e compare-os com o comportamento real das pessoas
  usuárias (por exemplo: "Você entrou mesmo à meia-noite, Dave?")
- procure sinais de persistência, como novas contas de usuário (por exemplo: "Quem é Elaine.Ransom?")

Isso vale para o próprio servidor TeamCity e também para qualquer outro servidor acessível a partir
dele, como os recursos de CI/CD.
