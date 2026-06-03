# Security Compliance Operations Engine for ISO 27001, SOC 2 Type II, PIPEDA, and Third-Party Risk

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [Solution Overview](#solution-overview)
- [Methodology](#methodology)
    - [Data Modeling](#data-modeling)
    - [Automation and Analysis](#automation-and-analysis)
    - [Reporting](#reporting)
- [Skills Used](#skills-used)
- [Repository Structure](#repository-structure)
- [Key Outputs and Results](#key-outputs-and-results)
- [Business Recommendations](#business-recommendations)
- [Next Steps](#next-steps)
- [Status](#status)
- [License](#license)
- [Author Info](#author-info)


[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Executive Summary

This project simulates the day-to-day work of a Senior Security Compliance Engineer operating governance, risk, and compliance processes for a cloud-native Canadian digital bank. The business problem is that audit readiness, evidence collection, policy governance, third-party risk, privacy operations, and management reporting often become fragmented, manual, and difficult to scale in high-growth regulated environments.

To address this, this project designs a lightweight compliance operations engine using Python, SQL, Power BI, and structured documentation. The solution models how a financial services organization can sustain ISO 27001 certification and SOC 2 Type II attestation, support PIPEDA-aligned privacy operations, manage vendor risk, and produce executive- and auditor-ready outputs through repeatable workflows rather than ad hoc effort.

The expected business impact is improved audit readiness, faster evidence retrieval, better visibility into remediation and residual risk, more structured privacy operations, and more defensible vendor oversight. Future iterations can extend this project into AWS-based evidence collection, customer security review automation, and trust center reporting.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Business Problem

In regulated cloud-native organizations, compliance failure is rarely caused by the absence of controls alone. More often, the problem is that evidence is stale, ownership is unclear, policy reviews slip, remediation items age without visibility, privacy requests are handled inconsistently, and third-party risk reviews are not operationalized in a scalable way.

For a digital bank, these issues create audit friction, increase regulatory exposure, weaken customer trust, and make it harder for leadership to understand the real security posture of the organization. The core business need is not just to “be compliant,” but to run compliance as an operational system that continuously produces usable evidence, accurate status reporting, and accountable follow-through.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Project Objectives

- Simulate the operating model of a Senior Security Compliance Engineer in a banking or fintech environment.
- Build a structured compliance data layer for controls, evidence, policies, risks, vendors, corrective actions, and privacy requests.
- Automate recurring compliance checks using Python and SQL.
- Produce management and audit-ready reporting through Power BI and markdown documentation.
- Demonstrate cross-framework thinking across ISO 27001, SOC 2 Type II, PIPEDA, and basic NIST CSF mappings.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Solution Overview

This repository represents a lightweight compliance operations engine for a fictional cloud-native Canadian digital bank called NorthStar Digital Bank. It is designed to show how governance, risk, and compliance processes can be organized into a repeatable system rather than a collection of disconnected spreadsheets and point-in-time documents.

The project includes:
- mock operational datasets for controls, evidence, risks, policies, vendors, and privacy workflows,
- Python scripts for automation of evidence freshness, policy reviews, remediation aging, vendor tiering, and privacy request monitoring,
- SQL queries for exception reporting and management review support,
- Power BI dashboards for control health, risk posture, vendor exposure, and privacy metrics,
- documentation artifacts such as audit evidence indexes, risk summaries, and privacy templates.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Methodology

The project is built using a combination of structured data modeling, automation, reporting, and operational documentation.

### Data Modeling
Mock datasets are created to represent the recurring workflows of a compliance function, including:
- control inventory,
- control test results,
- evidence register,
- policy register,
- risk register,
- corrective actions,
- vendor inventory and assessments,
- privacy requests,
- data inventory.

### Automation and Analysis
Python is used to automate recurring checks such as stale evidence detection, overdue policy reviews, remediation aging, residual risk scoring, vendor tiering, and privacy SLA tracking. SQL is used to build operational reporting views and support exception-based monitoring.

### Reporting
Power BI is used to create management-facing dashboards that summarize control status, open risks, overdue items, vendor exposure, and privacy operations. Markdown documentation is used to simulate auditor-ready and stakeholder-ready work products.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Skills Used

### Python
- pandas for data transformation and rule-based monitoring
- date-based logic for SLA and aging calculations
- CSV export automation
- exception reporting and compliance workflow checks

### SQL
- CTEs
- joins
- CASE logic
- aggregate functions
- filtering and grouping for operational reporting
- exception-based query design

### Power BI
- KPI cards
- status and aging visuals
- trend analysis
- risk heatmaps
- operational dashboards for leadership and audit support

### Governance, Risk, and Compliance
- ISO 27001 operating model concepts
- SOC 2 Type II evidence and control monitoring
- third-party risk management
- corrective action tracking
- policy lifecycle governance
- privacy operations aligned to PIPEDA
- basic NIST CSF mapping

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Repository Structure

```text
compliance-operations-engine/
├── README.md
├── data/
├── sql/
├── scripts/
├── dashboard/
├── docs/
└── outputs/
```

**Key folders:**
- `data/` stores mock operational datasets
- `sql/` stores reporting and monitoring queries
- `scripts/` stores Python automation
- `dashboard/` stores Power BI files and screenshots
- `docs/` stores business and audit-style documentation
- `outputs/` stores generated reports

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Key Outputs and Results

This project is designed to produce the following outputs:
- evidence freshness and missing evidence reports,
- overdue policy review tracking,
- residual risk prioritization,
- corrective action aging reports,
- vendor tiering and reassessment tracking,
- privacy request SLA monitoring,
- Power BI dashboards for executive and audit review,
- documentation that simulates management review, audit support, and customer-facing security responses.

The intended result is a portfolio project that demonstrates how compliance can be run as an operational engineering problem rather than as a manual documentation exercise.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Business Recommendations

The project is based on the idea that high-growth regulated organizations should treat compliance as a living operational system. Based on this approach, the key recommendations are:

- Centralize controls, evidence, risks, and vendors into a structured operating model.
- Automate recurring evidence and status checks wherever possible.
- Use dashboards to make remediation and residual risk visible to leadership.
- Tie privacy and third-party risk operations into the same oversight model rather than managing them separately.
- Design compliance outputs for multiple audiences: auditors, executives, customers, and internal stakeholders.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Next Steps

With more time, the next enhancements would include:
- integrating mock AWS configuration evidence,
- adding a trust center artifact register,
- building a customer security questionnaire response workflow,
- extending the framework mapping across ISO 27001, SOC 2, and NIST CSF,
- adding security awareness and phishing simulation metrics,
- simulating API-based evidence collection from identity and ticketing systems.

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Status

Current phase:
- [x] Day 1: Scenario, assumptions, backlog, and control domains
- [x] Day 2: Build compliance datasets
- [ ] Day 3: Build SQL monitoring layer
- [ ] Day 4: Build Python automation
- [ ] Day 5: Build risk scoring engine
- [ ] Day 6: Build third-party risk module
- [ ] Day 7: Build privacy operations module
- [ ] Day 8: Build Power BI dashboard
- [ ] Day 9: Final polish, screenshots, and interview packaging

[Back to Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## License

MIT License

Copyright (c) [2026] [Prasanna Sriram]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back to the Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)

---

## Author Info

- Github - [Github Profile](https://github.com/prasanna-sriram)
- LinkedIn - [Prasanna Sriram](https://www.linkedin.com/in/prasanna-sriram/)
- Tableau - [Tableau Public Profile](https://public.tableau.com/app/profile/prasanna.sriram.ps)

[Back to the Top](#security-compliance-operations-engine-for-iso-27001-soc-2-type-ii-pipeda-and-third-party-risk)