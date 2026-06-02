# Scenario: Compliance Operations Engine for a Canadian Digital Bank

---

## Company Profile

NorthStar Digital Bank is a fictional cloud-native Canadian financial services company that offers digital chequing accounts, savings products, small-business payment services, and embedded finance APIs for fintech partners. The organization operates as a high-growth, security-conscious institution that serves retail and commercial customers and processes sensitive personal, financial, and transactional data.

The company has a lean but maturing security and compliance function. It has already achieved ISO 27001 certification and SOC 2 Type II attestation, and now needs to sustain those programs through recurring evidence collection, internal audits, risk reviews, policy governance, third-party risk management, privacy operations, and management reporting.

This project simulates the day-to-day work of a Senior Security Compliance Engineer responsible for operating the compliance machinery that keeps those programs healthy, audit-ready, and scalable.

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Operating Regions

NorthStar Digital Bank operates primarily in Canada, with customer support, engineering, and security operations distributed across Canada and the United States. The company stores and processes customer and employee information connected to Canadian operations and also supports limited cross-border data handling for shared service operations, SaaS platforms, and support workflows.

Primary operating regions:
- Canada
- United States

Primary regulatory lens for this project:
- Canada-focused privacy and security expectations
- Cross-border data handling considerations for service providers and support functions

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Cloud-Native Environment Assumption

NorthStar Digital Bank is assumed to be a cloud-native organization with a modern SaaS-heavy operating model. Core banking-adjacent applications, internal productivity systems, ticketing platforms, identity systems, and evidence-producing operational systems are hosted in cloud environments or consumed as managed SaaS services.

For portfolio simplicity, this project does not build a live cloud environment. Instead, it simulates the compliance operations layer that would sit on top of such an environment, including:
- automated evidence collection logic,
- control monitoring outputs,
- policy and risk lifecycle tracking,
- vendor risk workflows,
- privacy request operations,
- audit and management reporting.

The architecture assumption is that evidence can be derived from systems such as identity providers, cloud logs, endpoint/security tooling, ticketing systems, HR systems, policy repositories, and vendor assurance records.

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Key Systems in Scope

The following systems are considered in scope for the simulated compliance program:

| **System** | **Purpose** | **Example Compliance Relevance** |
|------------|-------------|----------------------------------|
| Identity Provider | Workforce authentication and access control | MFA, joiner/mover/leaver controls, privileged access reviews |
| Cloud Infrastructure Platform | Hosting and infrastructure services | Logging, configuration management, backup, encryption, monitoring |
| Source Control / CI-CD Platform | Application development and deployment | Change management, secure deployment evidence, approval workflows |
| Ticketing / Workflow Platform | Change, incident, and request workflows | Evidence for approvals, remediation tracking, audit trail |
| HR Information System | Workforce lifecycle data | Access provisioning/deprovisioning, awareness training population |
| GRC / SharePoint-style Repository | Policies, risks, evidence, vendor records | Central compliance recordkeeping and audit readiness |
| Security Awareness Platform | Training and phishing simulation tracking | Completion status, campaign metrics, awareness evidence |
| Vendor Management Repository | Third-party inventory and assessments | Tiering, due diligence, remediation tracking |
| Customer Trust / Artifact Library | Customer-facing security artifacts | Security reviews, trust center upkeep |
| Privacy Operations Tracker | DSARs, privacy inquiries, retention tracking | PIPEDA operational support and accountability |

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Frameworks in Scope

This project models a compliance operating environment aligned to the following frameworks and regulatory obligations:

### ISO 27001

The project assumes the company operates an Information Security Management System (ISMS) aligned to ISO 27001. The simulated program includes activities such as risk assessment, risk treatment tracking, internal audit support, management review inputs, corrective action management, policy governance, and control evidence maintenance.

### SOC 2 Type II

The project assumes NorthStar Digital Bank maintains a SOC 2 Type II attestation focused on the Security criterion, with selected supporting controls relevant to availability, confidentiality, and privacy where applicable. The portfolio project emphasizes recurring evidence collection, control monitoring, remediation tracking, and audit-period reporting rather than a one-time point-in-time assessment.

### PIPEDA

The project includes privacy operations aligned to Canada’s Personal Information Protection and Electronic Documents Act (PIPEDA), including accountability for personal information handling, data inventories, privacy request handling, retention considerations, openness, safeguards, and support for individual access-related workflows.

### Basic NIST CSF Mapping

The project includes a lightweight mapping layer from operational controls into the NIST Cybersecurity Framework functions:
- Govern
- Identify
- Protect
- Detect
- Respond
- Recover

This mapping is included to demonstrate framework translation and control rationalization across compliance and cybersecurity reporting needs.

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Primary Stakeholders

- Security / Compliance
- Engineering
- IT
- HR
- Legal
- Procurement / Vendor Management
- Executive Leadership

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)

---

## Why This Scenario

This scenario is designed to imitate the real work of a Senior Security Compliance Engineer in a top banking or fintech environment. The role is not treated as policy administration alone; instead, it is modeled as an operational and analytical function that keeps audits, evidence, vendors, privacy processes, corrective actions, and management reporting running continuously.

[Back to Top](#scenario-compliance-operations-engine-for-a-canadian-digital-bank)