# Vendor Security Due Diligence Questionnaire

## Purpose

This questionnaire is used during vendor onboarding and periodic reassessment to evaluate a third party's security, privacy, and operational resilience posture prior to establishing or renewing a business relationship. Depth of review scales with the vendor's assigned risk tier per `docs/vendor-risk-methodology.md`.

**Vendor Name:** _______________________
**Service Provided:** _______________________
**Assessment Date:** _______________________
**Assigned Risk Tier:** ☐ High ☐ Medium ☐ Low
**Assessor:** _______________________

---

## Section 1: Access Control

1. Is multi-factor authentication (MFA) enforced for all administrative and privileged access to systems that process our data?
2. Describe your access provisioning and deprovisioning process, including timelines for revoking access after employee termination.
3. How frequently are user access rights reviewed, and by whom?
4. Do you enforce least-privilege access principles? Please describe.
5. Is role-based access control (RBAC) implemented for systems handling our data?

---

## Section 2: Encryption

1. Is data encrypted at rest? What encryption standard is used (e.g., AES-256)?
2. Is data encrypted in transit? What protocol is used (e.g., TLS 1.2+)?
3. How are encryption keys generated, stored, and rotated?
4. Do you use a dedicated key management system (KMS) or hardware security module (HSM)?

---

## Section 3: Logging and Monitoring

1. Are security-relevant events logged? What is the retention period for logs?
2. Do you have 24/7 monitoring or alerting for anomalous or unauthorized activity?
3. Are logs protected against unauthorized modification or deletion?
4. Do you conduct regular vulnerability scanning and penetration testing? How frequently?

---

## Section 4: Incident Response

1. Do you maintain a documented incident response plan? When was it last tested?
2. What is your committed timeline for notifying us in the event of a security incident or data breach affecting our data?
3. Have you experienced any security incidents or data breaches in the past 24 months? If so, please describe the nature and resolution.
4. Do you carry cyber liability insurance? What is the coverage amount?

---

## Section 5: Privacy

1. What categories of personal data does your service process, store, or transmit on our behalf?
2. Where is data stored and processed (data residency)? Does this include any locations outside Canada?
3. Do you have a documented data retention and secure disposal policy for data processed on our behalf?
4. How do you support data subject access, correction, or deletion requests routed through us?
5. Do you maintain a privacy policy aligned with applicable privacy laws (e.g., PIPEDA, GDPR)?

---

## Section 6: Subcontractors and Sub-processors

1. Do you use subcontractors or sub-processors with access to our data or systems?
2. If yes, please list all subcontractors/sub-processors and the services they provide.
3. Are subcontractors contractually bound to security and privacy requirements equivalent to your own commitments to us?
4. Will you notify us in advance of any change to your subcontractor/sub-processor list?

---

## Section 7: Certifications and Assurance

1. Do you hold any of the following certifications or attestations? (Check all that apply and provide most recent report/certificate date)
   - ☐ SOC 2 Type II — Date: _______
   - ☐ ISO 27001 — Date: _______
   - ☐ PCI DSS — Date: _______
   - ☐ Other: _______________________
2. Can you provide the most recent audit report or certificate upon request?

---

## Section 8: Business Continuity

1. Do you maintain a documented business continuity / disaster recovery plan?
2. What are your committed Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for the service provided to us?
3. When was your business continuity plan last tested?

---

## Assessor Summary

**Overall Risk Observation:** _______________________

**Open Findings Identified:** _______________________

**Recommended Follow-up Actions:** _______________________

**Next Review Due Date:** _______________________