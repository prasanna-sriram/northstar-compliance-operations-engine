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

To address this, this project designs a lightweight compliance operations engine using Python, SQL, Power BI, and structured documentation. The solution models how a financial services organization can sustain ISO 27001 certification and SOC 2 Type II attestation, support PIPEDA-aligned privacy operations, manage vendor risk, and produce executive and auditor-ready outputs through repeatable workflows rather than ad hoc effort.

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

This project is built incrementally, with each module producing working scripts, live CSV outputs, and supporting documentation rather than static placeholders. As of Day 6, the following modules are complete and validated against realistic mock data:

### Compliance Automation (Day 4)

Five Python scripts in `scripts/` read directly from `data/`, apply rule-based compliance logic, and write refreshed CSV reports to `outputs/` on every run:

| Script | Output | Purpose |
|--------|--------|---------|
| `evidence_freshness_check.py` | `overdue_evidence_report.csv` | Flags stale and missing control evidence |
| `policy_review_tracker.py` | `policy_review_status.csv` | Flags overdue and soon-due policy reviews |
| `remediation_tracker.py` | `remediation_aging_report.csv` | Buckets open corrective actions by age |
| `control_effectiveness_summary.py` | `control_effectiveness_summary.csv` | Summarizes pass/fail rates by domain and owner |
| `dsar_sla_monitor.py` | `dsar_status_report.csv` | Tracks privacy request SLA status |

### Risk Scoring Engine (Day 5)

`risk_scoring_engine.py` ranks all risks in the register by treatment urgency (residual score, boosted for overdue treatments), flags high-severity overdue risks for executive attention, and writes `outputs/risk_summary.csv`. This output feeds directly into `docs/management-review-summary.md`, connecting raw risk data to a leadership-ready report - a core ISO 27001 management review input.

### Third-Party Risk Module (Day 6)

`vendor_tiering.py` computes a weighted composite risk score (data sensitivity, business criticality, connectivity, privileged access) for all 35 vendors and independently derives a risk tier, rather than relying on static labels. Validated against the full vendor dataset, the engine:

- Scored and tiered all 35 vendors, flagging 14 as High tier.
- Identified 1 vendor overdue for reassessment and 10 flagged high priority (High tier combined with an overdue reassessment or open findings).
- Detected 4 cases of tier drift, where the calculated score disagreed with the vendor's originally assigned tier (e.g., a vendor labeled "High" recalculated as "Medium" once connectivity was scored as "Limited" rather than "Direct"). This demonstrates the practical value of a scoring engine over static vendor labels: it catches misclassifications that a manually maintained spreadsheet would miss.

Supporting documentation includes `docs/vendor-risk-methodology.md` (scoring methodology, tier definitions, due diligence depth, reassessment cadence) and a standalone `docs/vendor-due-diligence-questionnaire.md` covering access control, encryption, logging, incident response, privacy, and subcontractor management.

### Privacy Operations Module (Day 7)

`data/privacy_requests.csv` was enhanced with identity verification status, data sources searched, retention rule applied, residency, and lawful purpose fields to support a full PIPEDA-aligned DSAR workflow. Supporting documentation includes `docs/dsar-operating-procedure.md` (six-stage intake-to-closure workflow with SLA targets) and `docs/privacy-impact-assessment-template.md` for pre-launch privacy risk review. Re-running `dsar_sla_monitor.py` against the enhanced dataset flagged 4 of 30 requests as past due - consistent with the PIPEDA timeline risk (RISK-005) already identified in the Day 5 risk register.

### Planned Modules (Day 8–9)

- Power BI dashboard with executive, control operations, risk, vendor, and privacy views
- Audit evidence index and customer-facing security review pack

---

The intended result is a portfolio project that demonstrates how compliance can be run as an operational engineering problem - with working scripts, validated outputs, and traceable documentation - rather than as a manual documentation exercise.

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
- [x] Day 3: Build SQL monitoring layer
- [x] Day 4: Build Python automation
- [x] Day 5: Build risk scoring engine
- [x] Day 6: Build third-party risk module
- [x] Day 7: Build privacy operations module
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