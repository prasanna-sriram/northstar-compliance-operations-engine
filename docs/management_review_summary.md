# Management Review Summary

**Review Period:** Q3 2026 (as of July 24, 2026)
**Prepared By:** Prasanna Sriram, Senior Security Compliance Engineer
**Reviewed By:** Information Security Officer
**Date:** July 27, 2026

---

## Purpose

This memo summarizes the inputs required for the ISO 27001 management review, including top residual risks, overdue treatment items, recurring control gaps, status of prior review actions, and decisions requested from leadership. This review supports the ongoing determination of whether the ISMS remains suitable, adequate, and effective.

---

## Top 5 Residual Risks

Ranked by treatment urgency score (residual score, boosted for overdue treatments), sourced from `outputs/risk_summary.csv`.

| Rank | Risk | Category | Residual Score | Risk Level | Treatment Overdue | Owner |
|------|------|----------|-----------------|------------|--------------------|-------|
| 1 | Unauthorized access due to weak access controls | Access Management | 12 | High | Yes (24 days) | IT Operations |
| 2 | Insufficient logging leading to delayed incident detection | Monitoring | 8 | Medium | Yes (54 days) | Security Operations |
| 3 | Ransomware attack disrupting core banking availability | Cyber Security | 13 | High | No (due in 101 days) | Security Operations |
| 4 | Data breach from misconfigured cloud services | Cloud Security | 12 | High | No (due in 68 days) | Cloud Infrastructure |
| 5 | Outdated security policies misaligned with current environment | Governance | 6 | Medium | Yes (70 days) | Security Compliance |

**Key observation:** RISK-001 is the only risk currently flagged for executive attention (`executive_attention_flag = True`), because it combines a High risk level with an overdue treatment plan. RISK-011 (Ransomware) carries the highest residual score in the register (13) but is not yet flagged since its target date has not passed — this is worth watching closely given it's the single highest-severity risk on the register.

---

## Overdue Treatment Items

Four risk treatment plans have missed their target date and remain open or in progress:

| Risk | Category | Owner | Target Date | Days Overdue | Status |
|------|----------|-------|--------------|----------------|--------|
| RISK-001 — Unauthorized access due to weak access controls | Access Management | IT Operations | 2026-06-30 | 24 | In Progress |
| RISK-003 — Insufficient logging leading to delayed incident detection | Monitoring | Security Operations | 2026-05-31 | 54 | In Progress |
| RISK-008 — Outdated security policies misaligned with current environment | Governance | Security Compliance | 2026-05-15 | 70 | In Progress |
| RISK-005 — Failure to meet PIPEDA access request timelines | Privacy | Legal Privacy | 2026-04-30 | 85 | In Progress |

**Pattern:** All four overdue items are in "In Progress" status rather than stalled at "Open," indicating active work but slipping timelines. RISK-005 (privacy/PIPEDA) is the most overdue at 85 days and carries regulatory exposure, warranting priority follow-up with Legal Privacy.

---

## Recurring Control Gaps

Of 65 controls tested, 35 (54%) had a pass rate below 80%, and 9 of those recorded at least one outright Fail rather than only observations. This is a broader pattern than a handful of isolated findings and warrants structural attention rather than one-off remediation.

**Most severe gap:**

| Domain | Owner | Fail Count | Total Tests | Pass Rate |
|--------|-------|------------|--------------|-----------|
| Secure Software Development Lifecycle | Engineering | 2 | 2 | 0% |

This control failed both test cycles with zero passes, making it the single weakest control in the register and a priority for immediate remediation.

**Other controls with at least one Fail (50–67% pass rate):**

| Domain | Owner | Pass Rate |
|--------|-------|-----------|
| AML and KYC Data Handling | Legal Privacy | 50% |
| Data Classification and Loss Prevention | Security Operations | 50% |
| Privileged Access Management | Security Operations | 50% |
| Secure Configuration and Hardening | Cloud Infrastructure | 50% |
| SaaS Application Security Posture Management | IT Operations | 50% |
| Vulnerability Disclosure and Bug Bounty Program | Security Compliance | 50% |
| Privacy Request Handling and Data Retention Governance | Legal Privacy | 66.7% |
| Audit Evidence Management and Control Testing | Security Compliance | 66.7% |

**Ownership concentration:** Sub-80% pass rates are spread fairly evenly across five owning teams — Cloud Infrastructure, Legal Privacy, Security Compliance, and Security Operations each account for 6 of the 35 weak domains, and IT Operations accounts for 5. No single team is disproportionately responsible, suggesting this is a program-wide testing rigor issue rather than a team-specific performance problem.

**Direct linkage to risk register:** Several of these control gaps map directly to top residual risks flagged above. Privileged Access Management (50% pass rate, Security Operations) supports RISK-001 (unauthorized access, currently overdue and executive-flagged). Privacy Request Handling (66.7%, Legal Privacy) supports RISK-005 (PIPEDA timeline failures, 85 days overdue). This alignment between weak control test results and overdue risk treatments reinforces that these are not paperwork gaps — they reflect real operational exposure.

**Recommendation:** Prioritize remediation of the Secure Software Development Lifecycle control (0% pass rate) immediately, and schedule a targeted review of the eight controls with Fail results across Cloud Infrastructure, Legal Privacy, Security Compliance, and Security Operations within the next quarter.

---

## Actions from Prior Review

This is the first formal management review cycle documented for this ISMS. No prior review actions exist to track.

---

## Decisions Needed from Leadership

- [ ] Approve additional resourcing or reprioritization for IT Operations to close the 24-day-overdue access control treatment plan (RISK-001), currently the only executive-attention-flagged risk.
- [ ] Approve escalation of the DSAR/PIPEDA workflow gap (RISK-005) to Legal Privacy leadership given its 85-day overdue status and regulatory sensitivity.
- [ ] Approve a targeted review of the ransomware risk treatment plan (RISK-011) given it holds the highest residual score (13) on the register, even though it is not yet past its target date.
- [ ] Approve annual policy review calendar proposed under RISK-008 to prevent recurrence of policy governance lapses.

---

## Overall ISMS Effectiveness Assessment

Of the 30 risks in the register, 1 is currently flagged for executive attention and 4 have overdue treatment plans, representing roughly 13% of the register with active timeline slippage. No risk has reached "Critical" level (residual score ≥ 15), and the highest residual score observed is 13 (Ransomware, RISK-011), which remains within its treatment window. The concentration of overdue items in Access Management, Monitoring, Governance, and Privacy suggests these four domains should receive focused attention in the next review cycle. Overall, the ISMS appears to be operating with a manageable risk posture, but sustained tracking of the four overdue treatments is needed to prevent them from escalating into executive-attention items at the next scoring cycle.