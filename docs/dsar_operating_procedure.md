# DSAR Operating Procedure

## Purpose

This procedure defines the standard workflow for handling data subject access requests (DSARs) and related privacy requests (access, correction, deletion, complaint, inquiry) received by NorthStar Digital Bank, in alignment with PIPEDA's accountability, openness, and individual access principles.

---

## Workflow Stages

### 1. Intake

- Request is received via customer support, the privacy inbox, or a designated web form.
- Request is logged in `privacy_requests.csv` with a unique `request_id`, `request_type`, and `received_date`.
- `due_date` is calculated as `received_date + 30 calendar days`, consistent with PIPEDA's standard response timeline.
- Initial `status` is set to "Open."

### 2. Identity Verification

- Before any search or disclosure occurs, the requester's identity must be verified to prevent unauthorized disclosure of another individual's personal information.
- Acceptable verification methods: government-issued ID match against account records, security question challenge, or verified login session with MFA.
- `identity_verification_status` is set to "Verified," "Pending," or "Failed."
- If verification fails, the request is placed on hold and the requester is contacted for additional verification. A request should not proceed to search/discovery until verification is complete.

### 3. Search and Discovery

- Privacy team identifies all systems likely to hold the requester's personal data, referencing `data_inventory.csv` for system-level data type, PII classification, and ownership.
- Systems searched are logged in `data_sources_searched` (e.g., "Core Banking Platform, CRM, Identity Provider").
- Retrieved data is compiled into a working file for review, tagged with source system and record type.

### 4. Review and Redaction

- Compiled data is reviewed to ensure only the requester's own personal information is included — data belonging to other individuals (e.g., joint account holders, employees who handled the file) must be redacted.
- For deletion requests, retrieved data is cross-checked against `retention_rule_applied` to confirm whether a regulatory retention obligation overrides the deletion request (e.g., 7-year KYC/AML retention). If retention overrides deletion, the requester is informed of the specific legal basis.
- Legal or compliance sign-off is required before disclosure for any request involving financial, AML, or fraud-related records.

### 5. Response

- A formal response is prepared and delivered to the requester within the `due_date` window.
- Response includes: confirmation of identity verification, summary of data found (or confirmation no data exists), any applicable redactions and the reason, and — for deletion requests — an explanation of any data retained under regulatory obligation.
- Response method and delivery are logged.

### 6. Closure

- `status` is updated to "Closed" and `days_open` is finalized.
- The request record is retained per `retention_rule_applied` for audit and regulatory defensibility.
- If the request revealed a data inventory gap (e.g., data found in an unlisted system), the privacy team logs a follow-up item to update `data_inventory.csv`.

---

## SLA Targets

| Stage | Target Timeline |
|-------|-------------------|
| Identity verification | Within 5 business days of intake |
| Search and discovery | Within 15 business days of verified intake |
| Review and redaction | Within 5 business days of discovery completion |
| Final response | Within 30 calendar days of receipt (PIPEDA standard) |

Requests approaching or exceeding the 30-day window are tracked via `scripts/dsar_sla_monitor.py`, which classifies each open request as "On Track," "Due Soon" (within 7 days), or "Past Due."

---

## Escalation

- Any request with `identity_verification_status = Failed` after two verification attempts is escalated to the Legal Privacy owner for manual review.
- Any request past due per the SLA monitor output is escalated to the privacy team lead and noted in the next management review cycle.
- Complaints alleging a privacy breach or unauthorized disclosure are escalated immediately to the Information Security Officer, independent of standard DSAR timelines.

---

## Roles and Responsibilities

| Role | Responsibility |
|------|------------------|
| Privacy Team (Legal Privacy) | Intake, verification, search coordination, response drafting, closure |
| System Owners (per `data_inventory.csv`) | Support search/discovery within their system of record |
| Legal/Compliance | Sign-off on disclosures involving regulated data (AML, KYC, financial records) |
| Information Security Officer | Escalation point for suspected breaches or unauthorized disclosure complaints |