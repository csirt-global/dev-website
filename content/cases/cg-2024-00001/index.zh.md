---
title: "JetBrains TeamCity 身份验证绕过"
slug: "CG-2024-00001"
date: 2024-02-16
---

### 概要

近期在 TeamCity On-Premises 中发现了一个严重的安全漏洞。一旦被利用，未经授权且能通过 HTTP(S)
访问 TeamCity 服务器的攻击者即可绕过身份验证，进而取得受影响服务器的**管理员**权限，对系统的
完整性与安全性构成严重威胁。必须尽快处理并修复，以保障 TeamCity On-Premises 环境的机密性与
正常运行。

### 更新

JetBrains 建议 On-Prem 用户尽快升级到最新版本（2023.11.3），或者应用官方提供的安全补丁，以阻止
未授权访问。详情见其
[博客](https://blog.jetbrains.com/teamcity/2024/02/critical-security-issue-affecting-teamcity-on-premises-cve-2024-23917/)。

### 失陷排查

在条件允许的情况下，还应做一次失陷排查，确认该漏洞是否已被利用：

- 检查访问日志和审计日志，与真实用户的行为对照（例如：“Dave，你真的在半夜登录过吗？”）
- 查找持久化的痕迹，例如新增的用户账户（例如：“Elaine.Ransom 是谁？”）

排查范围既包括 TeamCity 服务器本身，也包括可从它访问到的其他服务器，例如 CI/CD 相关资产。
