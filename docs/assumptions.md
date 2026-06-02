# Assumptions

---

## Project Purpose

This project is a portfolio simulation of the operational work performed by a Senior Security Compliance Engineer in a Canadian digital banking environment. It is designed to demonstrate practical governance, risk, compliance, privacy, and third-party risk workflows using tools such as Python, SQL, and Power BI.

[Back to Top](#assumptions)

---

## Scope Assumptions

- The organization is a fictional digital bank with cloud-native and SaaS-heavy operations.
- The project represents the compliance operations layer, not a production banking system.
- The repository uses mock but realistic data to simulate controls, evidence, risks, vendors, policies, and privacy requests.
- The project focuses on operating the compliance program, not implementing deep security engineering controls directly.
- The primary compliance emphasis is sustainment: recurring evidence, audits, policy reviews, remediation, risk reviews, and reporting.

[Back to Top](#assumptions)

---

## Framework Assumptions

- ISO 27001 is treated as the primary ISMS framework.
- SOC 2 Type II is treated as a recurring attestation requiring evidence over time.
- PIPEDA is treated as the primary privacy compliance lens for Canadian operations.
- NIST CSF is used as a lightweight cross-framework mapping layer rather than a full standalone implementation.

[Back to Top](#assumptions)

---

## Technical Assumptions

- Python is used for automation and report generation.
- SQL is used for reporting logic, exception detection, and trend queries.
- Power BI is used for executive and operational dashboards.
- CSV and/or SQLite are sufficient for the simulated data layer.
- The project does not require a live AWS environment in the first version.
- Evidence-producing systems are represented through mock exports from source platforms rather than live API integrations.

[Back to Top](#assumptions)

---

## Operating Assumptions

- Controls are owned by named functions such as Security, IT, Engineering, HR, Legal, and Compliance.
- Evidence has defined collection frequencies and owners.
- Policies require scheduled review and version tracking.
- Risks require documented treatment plans, owners, and target dates.
- Vendors are tiered by inherent risk and reassessed on a periodic basis.
- Privacy requests are logged, assigned, and tracked against expected response timelines.
- Corrective actions are tracked to closure with effectiveness review.

[Back to Top](#assumptions)

---

## Data Assumptions

The repository will include mock datasets that simulate the following:
- controls and framework mappings,
- control test results,
- evidence inventory,
- policy register,
- risk register,
- corrective actions,
- vendor inventory and vendor assessments,
- privacy requests,
- data inventory and retention attributes.

[Back to Top](#assumptions)

---

## Delivery Assumptions

- The project will be built with regular GitHub commits.
- Each commit will result in a visible artifact such as a new dataset, script, document, dashboard component, or output file.
- The final repository should be understandable by recruiters, hiring managers, auditors, and security leaders.

[Back to Top](#assumptions)

---

## Key Control Domains

1. Information Security Policy Governance
2. Risk Assessment and Risk Treatment
3. Asset and Data Inventory Management
4. Identity and Access Management
5. Privileged Access Management
6. Authentication and MFA Enforcement
7. Logging and Security Monitoring
8. Vulnerability and Patch Management
9. Secure Configuration and Hardening
10. Change Management and Deployment Control
11. Backup, Recovery, and Resilience
12. Incident Response and Corrective Action Management
13. Third-Party Risk Management and Vendor Due Diligence
14. Privacy Request Handling and Data Retention Governance
15. Security Awareness and Phishing Simulation
16. Audit Evidence Management and Control Testing
17. Business Continuity and Operational Resilience
18. Customer Security Review and Trust Center Management

[Back to Top](#assumptions)

---

## Non-Goals

The following are intentionally out of scope for this version:
- production deployment,
- real customer data,
- live integrations with cloud providers or SaaS platforms,
- penetration testing,
- full legal interpretation of privacy law,
- a complete enterprise GRC platform replacement.

[Back to Top](#assumptions)