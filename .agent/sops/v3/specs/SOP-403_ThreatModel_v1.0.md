# SOP-403: Threat Modeling Guidelines

**Phase:** Architecture (Phase 4)
**Role:** Security Auditor

## Context
Security is not an add-on; it's a feature. We model threats BEFORE coding.

## STRIDE Methodology
We use Microsoft's STRIDE model.

| Threat | Property Violated | Mitigation |
| :--- | :--- | :--- |
| **S**poofing | Authentication | Strong Auth (MFA, JWT) |
| **T**ampering | Integrity | Checksums, Signatures |
| **R**epudiation | Non-repudiation | Audit Logs |
| **I**nformation Disclosure | Confidentiality | Encryption (TLS, AES) |
| **D**enial of Service | Availability | Rate Limiting, CDNs |
| **E**levation of Privilege | Authorization | RBAC, Principle of Least Privilege |

## Review
Threat models must be reviewed whenever architectural changes occur.
