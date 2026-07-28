# Privacy Impact Assessment (PIA) Template

## Purpose

This template is used to assess privacy risks associated with new products, features, systems, or data processing activities before launch, in alignment with PIPEDA's accountability principle and the privacy-by-design expectations reflected in `docs/vendor-risk-methodology.md` and the broader ISMS.

---

## Section 1: Project Overview

**Project/Feature Name:** _______________________
**Business Owner:** _______________________
**Assessment Date:** _______________________
**Assessor:** _______________________

**Brief description of the project, feature, or system:**

_______________________________________________________

---

## Section 2: Data Collection and Use

1. What personal data will be collected, used, or disclosed as part of this project?
2. What is the specific business purpose for collecting this data? (Reference `lawful_purpose` conventions used in `data_inventory.csv`.)
3. Is the data collection limited to what is necessary for the stated purpose (data minimization)?
4. Will any new categories of personal data be collected that are not already tracked in `data_inventory.csv`?
5. Will consent be obtained from individuals, and if so, how?

---

## Section 3: Data Flow and Storage

1. Where will the data be stored? (System name, cloud region, residency)
2. Will data be transmitted to or stored in any location outside Canada? If so, what cross-border transfer safeguards apply?
3. Will any third-party vendors process this data? If yes, reference the applicable vendor risk tier from `outputs/vendor_risk_summary.csv`.
4. What is the data retention period, and what is the secure disposal process at end of retention?

---

## Section 4: Access and Security Controls

1. Who will have access to this data, and is access restricted on a least-privilege basis?
2. Is the data encrypted at rest and in transit?
3. Will this data be subject to existing logging and monitoring controls?
4. Does this project introduce any new attack surface (e.g., new API, new integration) that requires a security review?

---

## Section 5: Individual Rights Impact

1. Will individuals be able to exercise access, correction, and deletion rights over this data through the existing DSAR process (`docs/dsar-operating-procedure.md`)?
2. Does this project affect the accuracy or timeliness of responses to privacy requests?
3. Will individuals be notified about this data collection/use, and how?

---

## Section 6: Risk Identification

| Risk Description | Likelihood | Impact | Mitigation |
|--------------------|------------|--------|-------------|
| | | | |
| | | | |

---

## Section 7: Assessment Outcome

**Overall privacy risk level:** ☐ Low ☐ Medium ☐ High

**Conditions required before launch (if any):**

_______________________________________________________

**Approval:**

- Privacy Team Sign-off: _______________________ Date: _______
- Security Team Sign-off (if applicable): _______________________ Date: _______
- Business Owner Acknowledgment: _______________________ Date: _______