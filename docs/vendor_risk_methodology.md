# Vendor Risk Methodology

## Purpose

This document defines how NorthStar Digital Bank classifies third-party vendors into risk tiers, sets due diligence depth and reassessment cadence per tier, and establishes remediation expectations for open findings. This methodology supports SOC 2's requirement for a documented vendor classification and review process, and ISO 27001 Annex A.5.19–5.22 (supplier relationship security).

---

## Scoring Dimensions

Each vendor receives a weighted composite risk score (0–100) based on four factors:

| Factor | Weight | Scale |
|--------|--------|-------|
| Data sensitivity | 30% | High = 4, Medium = 2, Low = 1 |
| Business criticality | 30% | High = 4, Medium = 2, Low = 1 |
| Connectivity / integration depth | 20% | Direct = 3, Limited = 2, None = 0 |
| Privileged access to systems/data | 20% | Yes = 3, No = 0 |

**Data sensitivity** reflects the type of data the vendor can access (e.g., customer PII, financial data, credentials). **Business criticality** reflects the operational impact if the vendor's service fails or is compromised. **Connectivity** reflects how deeply the vendor is integrated into production systems (direct API/system access vs. limited or no technical connectivity). **Privileged access** reflects whether vendor personnel or systems hold elevated or administrative access.

Each factor is normalized to its own maximum before weighting, so the final composite score always falls on a consistent 0–100 scale regardless of how many factors apply.

---

## Risk Tiers

| Tier | Composite Score | Description |
|------|-------------------|-------------|
| High | 70–100 | Vendor has significant access to sensitive data, deep system integration, or high business criticality (e.g., core banking software, payment processors, cloud infrastructure). |
| Medium | 40–69 | Vendor has moderate exposure — limited data access or partial integration (e.g., CRM, payroll, contact center tooling). |
| Low | 0–39 | Vendor has minimal data access, no system connectivity, and low criticality (e.g., translation services, general consulting). |

---

## Due Diligence Depth by Tier

| Tier | Onboarding Due Diligence | Ongoing Monitoring |
|------|---------------------------|----------------------|
| High | Full security questionnaire, SOC 2/ISO evidence review, architecture and data flow review, contract security addendum, executive sign-off | Continuous monitoring where available; annual reassessment mandatory |
| Medium | Standard security questionnaire, evidence of certifications if applicable, standard contract clauses | Annual or 18-month reassessment depending on criticality trend |
| Low | Lightweight questionnaire or self-attestation, standard contract terms | Reassessment every 24 months, or upon material change in scope |

---

## Reassessment Cadence

| Tier | Cadence |
|------|---------|
| High | Every 12 months |
| Medium | Every 18 months |
| Low | Every 24 months |

Vendors flagged as `reassessment_overdue = True` in `outputs/vendor_risk_summary.csv` have exceeded their tier's cadence and require immediate scheduling of a renewed review, regardless of their last security score.

---

## Remediation Expectations

- **Open findings on High-tier vendors** must have a remediation plan with a target date within 60 days of identification, tracked in `corrective_actions.csv` if the finding originates internally, or via vendor-provided remediation evidence if the finding originates from the vendor's own assessment.
- **Open findings on Medium-tier vendors** should have a remediation plan within 90 days.
- **Open findings on Low-tier vendors** are tracked but do not require a formal remediation SLA unless the finding materially changes the vendor's risk profile (in which case the vendor should be re-tiered).
- Vendors with a `high_priority_flag = True` (High tier, combined with overdue reassessment or unresolved findings) should be escalated to the vendor risk owner and reviewed at the next management review cycle.

---

## Example Review Criteria

When conducting a vendor review, evaluate and document:

- **Access control**: MFA enforcement, least-privilege access, access review cadence
- **Encryption**: Data encrypted in transit and at rest, key management practices
- **Logging and monitoring**: Security event logging, retention period, incident detection capability
- **Incident response**: Documented IR plan, breach notification commitments, past incident history
- **Privacy**: Data handling practices, sub-processor disclosure, data residency commitments
- **Subcontractors**: Whether the vendor uses subcontractors/sub-processors, and whether those are disclosed and assessed

---

## Known Observations

- VEND-020 (Background Check Screening Vendor) carries 4 open findings but is classified Low tier under the current model, since its connectivity and criticality are low. Per methodology, Low-tier findings do not carry a mandatory remediation SLA, but a manual review is recommended given the finding count is unusually high for this tier.