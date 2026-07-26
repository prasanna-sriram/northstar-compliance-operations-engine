"""
expand_datasets.py
-------------------------------------------------------------------------------
Purpose: Expand the compliance-operations-engine mock datasets to a realistic
         scale for a cloud-native Canadian digital bank, while preserving all
         existing rows, ID sequences, and referential integrity across files.

Usage:
    1. Place this script in the root of your repo (same level as data/).
    2. Run: python expand_datasets.py
    3. It reads existing CSVs from data/, appends realistic new rows, and
       overwrites each file in data/ with the expanded, combined dataset.

Design principles:
    - Existing rows are never modified or removed.
    - New IDs continue the existing numbering sequence (e.g. CTRL-019 onward).
    - New controls automatically get matching framework_mapping rows, plus
      evidence_inventory and control_tests rows scaled to test_frequency.
    - New vendors automatically get vendor_assessment rows.
    - Dates are generated relative to a fixed "as of" date so re-running the
      script produces consistent, reproducible output.

Expected approximate row counts after running (existing + new):
    controls.csv            18 + 47 = 65
    framework_mapping.csv   18 + 47 = 65
    control_tests.csv       21 + ~110-130 = ~130-150
    evidence_inventory.csv  27 + 130 = ~157
    vendors.csv             10 + 25 = 35
    vendor_assessment.csv   11 + 35 = 46
    policy_register.csv     10 + 15 = 25
    risk_register.csv       10 + 20 = 30
    corrective_actions.csv  8  + 12 = 20
    privacy_requests.csv    10 + 20 = 30
    data_inventory.csv      10 + 10 = 20
-------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

DATA_DIR = "data/"
AS_OF = datetime(2026, 7, 24)


def load(name):
    """Load an existing CSV from data/, or return an empty DataFrame if missing."""
    try:
        return pd.read_csv(DATA_DIR + name)
    except FileNotFoundError:
        return pd.DataFrame()


def next_num(df, id_col):
    """Determine the next available numeric suffix for a given ID column."""
    if df is None or df.empty:
        return 1
    nums = df[id_col].str.extract(r"(\d+)$")[0].astype(int)
    return nums.max() + 1


def rand_date_between(days_ago_start, days_ago_end):
    """Random date between (AS_OF - days_ago_start) and (AS_OF - days_ago_end)."""
    d1 = AS_OF - timedelta(days=days_ago_start)
    d2 = AS_OF - timedelta(days=days_ago_end)
    if d1 > d2:
        d1, d2 = d2, d1
    delta = (d2 - d1).days
    return d1 + timedelta(days=random.randint(0, max(delta, 0)))


def fmt(d):
    return d.strftime("%Y-%m-%d")


FREQ_DAYS = {
    "Monthly": 30, "Quarterly": 90, "Semi-Annual": 182, "Annual": 365,
}

TESTERS = ["Security Compliance", "Internal Audit", "Security Operations",
           "Cloud Infrastructure", "Engineering", "IT Operations", "HR",
           "Legal Privacy", "Business Continuity"]

RESULT_WEIGHTS = [("Pass", 0.78), ("Pass with Observation", 0.16), ("Fail", 0.06)]

ISSUE_TEXT = {
    "Pass": "No material issues noted",
    "Pass with Observation": "Minor gap identified; tracked for follow-up",
    "Fail": "Control did not operate as designed; corrective action initiated",
}

SOURCE_SYSTEMS = ["Document Repository", "Identity Provider", "Ticketing Platform",
                   "SIEM", "Vulnerability Scanner", "Cloud Logs", "Backup Platform",
                   "HRIS", "Vendor Management Portal", "Privacy Tracker",
                   "Security Awareness Platform", "CMDB", "Cloud Infrastructure Console"]


# ==============================================================================
# 1. CONTROLS + FRAMEWORK MAPPING  (existing 18 -> 65 total)
# ==============================================================================
controls_df = load("controls.csv")
fmap_df = load("framework_mapping.csv")

# (domain, control_name, owner, test_frequency, evidence_required,
#  iso_clause, iso_annex_a_control, soc2_tsc, nist_csf_function)
NEW_CONTROL_SPECS = [
    ("Cryptography and Key Management", "Encryption keys are generated, stored, rotated, and retired using approved cryptographic standards.", "Cloud Infrastructure", "Quarterly", "Key rotation log and KMS configuration export", "5.2; 9.3", "A.8.24 Use of Cryptography", "CC6.1; CC6.7", "PROTECT"),
    ("Network Security and Segmentation", "Network zones are segmented by trust level and monitored for unauthorized traffic between segments.", "Cloud Infrastructure", "Quarterly", "Network segmentation diagram and firewall rule review", "8.1", "A.8.20 Networks Security; A.8.22 Segregation of Networks", "CC6.6; CC6.7", "PROTECT"),
    ("Secure Software Development Lifecycle", "Application code is reviewed for security defects prior to production deployment.", "Engineering", "Monthly", "Code review records and SAST/DAST scan results", "8.1; 8.25", "A.8.25 Secure Development Life Cycle; A.8.28 Secure Coding", "CC8.1", "PROTECT"),
    ("Endpoint and Mobile Device Management", "Workforce endpoints and mobile devices are enrolled in MDM with encryption and remote wipe capability.", "IT Operations", "Quarterly", "MDM compliance report", "8.1", "A.8.1 User Endpoint Devices", "CC6.6", "PROTECT"),
    ("Physical and Data Center Security", "Cloud provider and any physical facilities maintain access controls, surveillance, and environmental safeguards.", "Cloud Infrastructure", "Annual", "Data center SOC 2 report and physical access log review", "7.1; 7.2", "A.7.1 Physical Security Perimeter; A.7.2 Physical Entry", "CC6.4", "PROTECT"),
    ("API Security and Rate Limiting", "APIs enforce authentication, authorization, input validation, and rate limiting to prevent abuse.", "Engineering", "Monthly", "API gateway configuration export and abuse detection log", "8.1", "A.8.26 Application Security Requirements", "CC6.1; CC6.6", "PROTECT"),
    ("Cloud Shared Responsibility Management", "Cloud provider security responsibilities are documented and periodically validated against the shared responsibility model.", "Cloud Infrastructure", "Semi-Annual", "Cloud provider attestation review and responsibility matrix", "8.1; 5.2", "A.5.23 Information Security for Use of Cloud Services", "CC1.4; CC6.1", "GOVERN"),
    ("Data Classification and Loss Prevention", "Sensitive data is classified and monitored with DLP controls to prevent unauthorized exfiltration.", "Security Operations", "Quarterly", "Data classification policy review and DLP alert summary", "5.12; 8.1", "A.5.12 Classification of Information; A.8.11 Data Masking", "CC6.7", "PROTECT"),
    ("Fraud Monitoring and Transaction Controls", "Transaction monitoring rules detect and flag potentially fraudulent account activity for review.", "Security Operations", "Monthly", "Fraud rule tuning log and case disposition summary", "8.1", "A.8.16 Monitoring Activities", "CC7.2", "DETECT"),
    ("AML and KYC Data Handling", "Customer identity verification and AML screening data is handled according to regulatory retention and access requirements.", "Legal Privacy", "Quarterly", "AML data handling review and access log export", "8.1; 5.34", "A.5.34 Privacy and Protection of PII", "P1.1; P2.1", "PROTECT"),
    ("Insider Threat Monitoring", "User behavior analytics and access anomaly detection are used to identify potential insider risk.", "Security Operations", "Monthly", "UBA alert review log", "8.1", "A.8.16 Monitoring Activities", "CC7.2", "DETECT"),
    ("Capacity and Availability Management", "System capacity is monitored and forecasted to maintain service availability under peak load.", "Cloud Infrastructure", "Quarterly", "Capacity utilization report and scaling event log", "8.6", "A.8.6 Capacity Management", "A1.1", "PROTECT"),
    ("Secure Remote Access", "Remote workforce access is authenticated via VPN or zero-trust access with device posture checks.", "IT Operations", "Quarterly", "Remote access log and device posture compliance report", "8.1", "A.8.20 Networks Security", "CC6.6", "PROTECT"),
    ("Data Loss Prevention for Email and Endpoints", "Outbound email and endpoint data transfers are scanned for sensitive data leakage.", "Security Operations", "Monthly", "DLP incident report", "8.1", "A.8.12 Data Leakage Prevention", "CC6.7", "PROTECT"),
    ("Penetration Testing and Red Team Exercises", "Independent penetration tests are performed against critical systems on a periodic basis.", "Security Compliance", "Annual", "Penetration test report and remediation tracker", "8.29", "A.8.29 Security Testing in Development and Acceptance", "CC4.1", "IDENTIFY"),
    ("Secrets and Credential Management", "Application secrets and service credentials are stored in a managed vault and rotated periodically.", "Cloud Infrastructure", "Quarterly", "Secrets vault access report and rotation log", "8.1", "A.8.24 Use of Cryptography", "CC6.1", "PROTECT"),
    ("Container and Orchestration Security", "Container images are scanned for vulnerabilities and orchestration platforms are hardened per baseline.", "Cloud Infrastructure", "Monthly", "Container scan report and orchestration config review", "8.1", "A.8.9 Configuration Management", "CC7.1", "PROTECT"),
    ("Third-Party Software Bill of Materials Management", "Open-source and third-party software components are inventoried and monitored for known vulnerabilities.", "Engineering", "Quarterly", "SBOM export and vulnerability scan cross-reference", "8.1", "A.8.28 Secure Coding", "CC7.1", "IDENTIFY"),
    ("Data Residency and Cross-Border Transfer Controls", "Data storage and processing locations are validated against residency commitments and cross-border transfer rules.", "Legal Privacy", "Semi-Annual", "Data residency attestation and transfer mechanism review", "5.34", "A.5.34 Privacy and Protection of PII", "P6.1", "GOVERN"),
    ("Mobile Application Security", "Mobile banking application releases undergo security testing prior to publication.", "Engineering", "Quarterly", "Mobile app security test report", "8.29", "A.8.29 Security Testing in Development and Acceptance", "CC8.1", "PROTECT"),
    ("Email Authentication and Anti-Phishing Controls", "Email domains enforce SPF, DKIM, and DMARC, and inbound mail is scanned for phishing indicators.", "IT Operations", "Quarterly", "Email authentication config report and phishing filter log", "8.1", "A.8.23 Web Filtering", "CC6.6", "PROTECT"),
    ("Disaster Recovery Planning", "A documented disaster recovery plan defines recovery time and point objectives for critical systems.", "Business Continuity", "Semi-Annual", "DR plan document and tabletop exercise summary", "5.30; 8.1", "A.5.30 ICT Readiness for Business Continuity", "A1.2; A1.3", "RECOVER"),
    ("Segregation of Duties", "Critical financial and administrative functions require dual control or segregation to prevent unilateral action.", "Security Compliance", "Annual", "Segregation of duties matrix and exception log", "5.3", "A.5.3 Segregation of Duties", "CC5.1", "GOVERN"),
    ("Vulnerability Disclosure and Bug Bounty Program", "External researchers can report vulnerabilities through a defined and monitored disclosure channel.", "Security Compliance", "Quarterly", "Bug bounty submission log and triage summary", "8.8", "A.8.8 Management of Technical Vulnerabilities", "CC7.1", "DETECT"),
    ("Open Banking and API Partner Governance", "Third-party API consumers and open banking partners are validated and monitored for compliant data usage.", "Security Compliance", "Quarterly", "Partner API access review and usage audit", "5.19", "A.5.19 Information Security in Supplier Relationships", "CC9.2", "GOVERN"),
    ("Data Retention and Secure Disposal", "Data is retained per policy and securely disposed of when retention periods expire.", "Legal Privacy", "Quarterly", "Disposal certificate log and retention compliance report", "8.10", "A.8.10 Information Deletion", "P4.1; P4.2", "PROTECT"),
    ("Security Governance and Steering Committee", "A cross-functional security steering committee reviews program performance and approves key decisions.", "Executive Leadership", "Quarterly", "Steering committee meeting minutes", "5.1", "A.5.1 Policies for Information Security", "CC1.1", "GOVERN"),
    ("Model Risk Management for Fraud and Credit Models", "Automated decisioning models are validated, monitored for drift, and reviewed for bias.", "Security Compliance", "Semi-Annual", "Model validation report and drift monitoring summary", "8.1", "A.8.16 Monitoring Activities", "CC3.2", "IDENTIFY"),
    ("Contractor and Third-Party Personnel Access", "Contractor and temporary personnel access is provisioned, time-boxed, and reviewed separately from employees.", "IT Operations", "Quarterly", "Contractor access review report", "6.1", "A.6.1 Screening", "CC6.2", "PROTECT"),
    ("Security Metrics and KPI Reporting", "Security and compliance KPIs are collected, tracked, and reported to leadership on a defined cadence.", "Security Compliance", "Monthly", "KPI dashboard export and reporting log", "9.1", "A.5.35 Independent Review of Information Security", "CC4.1", "GOVERN"),
    ("Customer Authentication and Fraud Controls for Digital Channels", "Digital banking channels enforce step-up authentication for high-risk transactions.", "Engineering", "Monthly", "Step-up authentication trigger log", "8.1", "A.8.5 Secure Authentication", "CC6.1", "PROTECT"),
    ("Data Backup Encryption and Integrity Verification", "Backup data is encrypted at rest and integrity-checked to detect corruption or tampering.", "Cloud Infrastructure", "Quarterly", "Backup encryption config and integrity check report", "8.1", "A.8.13 Information Backup", "A1.2", "RECOVER"),
    ("Regulatory Change Management", "Regulatory developments across operating jurisdictions are tracked and translated into control or policy updates.", "Legal Privacy", "Quarterly", "Regulatory tracking log and control change record", "5.31", "A.5.31 Legal, Statutory, Regulatory and Contractual Requirements", "CC1.3", "GOVERN"),
    ("Employee Offboarding and Access Revocation", "Departing employee access is revoked across all systems within a defined SLA of termination.", "IT Operations", "Monthly", "Offboarding ticket sample and access revocation timestamp report", "6.5", "A.6.5 Responsibilities After Termination", "CC6.2", "PROTECT"),
    ("Threat Intelligence Integration", "External threat intelligence feeds are integrated into monitoring to improve detection of known threat indicators.", "Security Operations", "Monthly", "Threat intel feed integration log and IOC match report", "5.7", "A.5.7 Threat Intelligence", "CC7.2", "DETECT"),
    ("Data Subject Rights Fulfillment Controls", "Systems support timely search, extraction, and deletion of personal data to fulfill privacy rights requests.", "Legal Privacy", "Quarterly", "DSAR fulfillment system capability review", "5.34", "A.5.34 Privacy and Protection of PII", "P3.1; P3.2", "PROTECT"),
    ("Cloud Cost and Resource Governance", "Cloud resource provisioning is governed by tagging, budget, and approval controls to prevent shadow IT.", "Cloud Infrastructure", "Quarterly", "Resource tagging compliance report and budget exception log", "5.9", "A.5.9 Inventory of Information and Other Associated Assets", "CC6.1", "IDENTIFY"),
    ("Customer Notification and Breach Communication", "A defined process governs timely customer and regulator notification in the event of a confirmed data breach.", "Legal Privacy", "Annual", "Breach notification runbook and tabletop exercise record", "5.24; 5.26", "A.5.26 Response to Information Security Incidents", "CC7.4", "RESPOND"),
    ("Encryption in Transit Enforcement", "All data transmitted between systems and to customers is encrypted using approved TLS configurations.", "Cloud Infrastructure", "Quarterly", "TLS configuration scan report", "8.24", "A.8.24 Use of Cryptography", "CC6.7", "PROTECT"),
    ("Security Awareness for Executives and Board Reporting", "Executives and board members receive tailored security briefings to support governance oversight.", "Security Compliance", "Semi-Annual", "Board security briefing deck and attendance record", "5.1; 7.2", "A.6.3 Information Security Awareness, Education and Training", "CC1.1", "GOVERN"),
    ("Data Minimization in Product Design", "New product and feature designs are reviewed to ensure only necessary personal data is collected and processed.", "Legal Privacy", "Quarterly", "Privacy-by-design review checklist sample", "5.34", "A.5.34 Privacy and Protection of PII", "P1.1", "GOVERN"),
    ("Incident Response Tabletop Exercises", "Simulated incident response exercises validate readiness and identify process gaps across teams.", "Security Compliance", "Semi-Annual", "Tabletop exercise report and after-action items", "5.24", "A.5.24 Information Security Incident Management Planning and Preparation", "CC7.3", "RESPOND"),
    ("SaaS Application Security Posture Management", "SaaS application configurations are continuously monitored for security misconfigurations.", "IT Operations", "Monthly", "SaaS security posture scan report", "8.9", "A.8.9 Configuration Management", "CC6.6", "PROTECT"),
    ("Data Encryption Key Access Restriction", "Access to encryption key management systems is restricted to authorized personnel with logged approval.", "Cloud Infrastructure", "Quarterly", "KMS access control review", "8.24", "A.8.24 Use of Cryptography", "CC6.1", "PROTECT"),
    ("Vendor Offboarding and Data Return/Destruction", "Terminated vendor relationships include verified data return or destruction and access revocation.", "Procurement", "Quarterly", "Vendor offboarding checklist and destruction certificate", "5.20", "A.5.20 Addressing Information Security Within Supplier Agreements", "CC9.2", "GOVERN"),
    ("Application Logging Standards Compliance", "Application logs conform to defined standards for content, retention, and tamper resistance.", "Engineering", "Quarterly", "Log standard compliance sample review", "8.15", "A.8.15 Logging", "CC7.2", "DETECT"),
    ("Privileged Session Recording", "Sessions using privileged or administrative access to production systems are recorded for audit purposes.", "Security Operations", "Monthly", "Session recording coverage report", "8.15", "A.8.15 Logging", "CC7.2", "DETECT"),
    ("Data Anonymization and Pseudonymization for Analytics", "Data used for analytics and testing is anonymized or pseudonymized to reduce privacy risk.", "Product Analytics", "Quarterly", "Anonymization technique validation report", "8.11", "A.8.11 Data Masking", "P8.1", "PROTECT"),
]

controls_start = next_num(controls_df, "control_id")
controls_rows, fmap_rows = [], []
for i, spec in enumerate(NEW_CONTROL_SPECS):
    cid = f"CTRL-{controls_start + i:03d}"
    domain, name, owner, freq, evidence_req, iso_clause, annex, soc2, nist_fn = spec
    controls_rows.append({
        "control_id": cid, "framework": "ISO 27001 / SOC 2", "domain": domain,
        "control_name": name, "owner": owner, "test_frequency": freq,
        "evidence_required": evidence_req, "status": "Active",
    })
    fmap_rows.append({
        "control_id": cid, "iso_clause": iso_clause, "iso_annex_a_control": annex,
        "soc2_tsc": soc2, "nist_csf_function": nist_fn,
        "control_objective": f"Ensure {domain.lower()} practices are implemented, monitored, and evidenced.",
    })

controls_out = pd.concat([controls_df, pd.DataFrame(controls_rows)], ignore_index=True)
fmap_out = pd.concat([fmap_df, pd.DataFrame(fmap_rows)], ignore_index=True)
controls_out.to_csv(DATA_DIR + "controls.csv", index=False)
fmap_out.to_csv(DATA_DIR + "framework_mapping.csv", index=False)
print(f"controls.csv -> {len(controls_out)} rows")
print(f"framework_mapping.csv -> {len(fmap_out)} rows")


# ==============================================================================
# 2. CONTROL TESTS  (existing -> ~130-150 total, capped at 2 cycles/control)
# ==============================================================================
tests_df = load("control_tests.csv")
if tests_df.empty:
    tests_df = load("controls_tests.csv")  # handle legacy filename

test_rows = []
tnum = next_num(tests_df, "test_id")
for _, row in controls_out.iterrows():
    cid = row["control_id"]
    freq = row["test_frequency"]
    interval = FREQ_DAYS.get(freq, 90)
    cycles = max(365 // interval, 1)
    cycles = min(cycles, 2)  # cap at 2 cycles per control for a realistic total
    for c in range(cycles):
        days_ago_start = interval * (c + 1)
        days_ago_end = interval * c
        test_date = rand_date_between(days_ago_start + 200, days_ago_end + 200)
        r = random.random()
        cumulative = 0.0
        result = "Pass"
        for label, weight in RESULT_WEIGHTS:
            cumulative += weight
            if r <= cumulative:
                result = label
                break
        test_rows.append({
            "test_id": f"TEST-{tnum:03d}",
            "control_id": cid,
            "test_date": fmt(test_date),
            "tester": random.choice(TESTERS),
            "result": result,
            "issues_found": ISSUE_TEXT[result],
        })
        tnum += 1

tests_out = pd.concat([tests_df, pd.DataFrame(test_rows)], ignore_index=True)
tests_out.to_csv(DATA_DIR + "control_tests.csv", index=False)
print(f"control_tests.csv -> {len(tests_out)} rows")


# ==============================================================================
# 3. EVIDENCE INVENTORY  (existing -> ~157 total, 2 artifacts per control)
# ==============================================================================
evidence_df = load("evidence_inventory.csv")
evidence_rows = []
enum_ = next_num(evidence_df, "evidence_id")
ARTIFACT_SUFFIXES = ["primary evidence export", "supporting log extract", "review sign-off record"]

for _, row in controls_out.iterrows():
    cid = row["control_id"]
    owner = row["owner"]
    freq = row["test_frequency"]
    interval = FREQ_DAYS.get(freq, 90)
    n_artifacts = 2  # 2 artifacts per control
    for a in range(n_artifacts):
        last_collected = rand_date_between(interval + 30, 5)
        next_due = last_collected + timedelta(days=interval)
        days_from_now = (next_due - AS_OF).days
        if days_from_now < 0:
            status = "Overdue"
        elif days_from_now <= 14:
            status = "Due Soon"
        else:
            status = "Current"
        evidence_rows.append({
            "evidence_id": f"EVID-{enum_:03d}",
            "control_id": cid,
            "evidence_name": f"{row['evidence_required'].split(' and ')[0]} - {ARTIFACT_SUFFIXES[a % 3]}",
            "source_system": random.choice(SOURCE_SYSTEMS),
            "owner": owner,
            "last_collected_date": fmt(last_collected),
            "next_due_date": fmt(next_due),
            "status": status,
        })
        enum_ += 1

evidence_out = pd.concat([evidence_df, pd.DataFrame(evidence_rows)], ignore_index=True)
evidence_out.to_csv(DATA_DIR + "evidence_inventory.csv", index=False)
print(f"evidence_inventory.csv -> {len(evidence_out)} rows")


# ==============================================================================
# 4. VENDORS  (existing 10 -> 35 total)
# ==============================================================================
vendors_df = load("vendors.csv")

NEW_VENDORS = [
    ("Core Banking Software Provider", "Core Banking Software", "High", "Direct", "High", "Yes", "High"),
    ("Card Network Payment Processor", "Payment Processing", "High", "Direct", "High", "Yes", "High"),
    ("KYC Identity Verification Service", "Identity Verification", "High", "Direct", "High", "No", "High"),
    ("AML Transaction Monitoring Platform", "AML/Fraud Monitoring", "High", "Direct", "High", "No", "High"),
    ("Fraud Detection and Risk Scoring Vendor", "Fraud Detection", "High", "Direct", "High", "No", "High"),
    ("SMS and OTP Delivery Provider", "Communications", "Medium", "Direct", "Medium", "No", "Medium"),
    ("Cloud Infrastructure Provider", "Cloud Hosting (IaaS)", "High", "Direct", "High", "Yes", "High"),
    ("Customer Support CRM Platform", "CRM / Customer Support", "Medium", "Limited", "Medium", "No", "Medium"),
    ("Marketing Automation and Email Platform", "Marketing Technology", "Low", "Limited", "Low", "No", "Low"),
    ("Background Check Screening Vendor", "HR Screening", "Medium", "Limited", "Low", "No", "Medium"),
    ("Independent Penetration Testing Firm", "Security Testing", "Medium", "Limited", "Medium", "Yes", "Medium"),
    ("Disaster Recovery Site Provider", "DR / Business Continuity", "High", "Direct", "High", "No", "High"),
    ("Open Banking API Aggregator Partner", "API Aggregation", "High", "Direct", "High", "No", "High"),
    ("Credit Bureau Data Provider", "Credit Data", "High", "Limited", "Medium", "No", "High"),
    ("Data Labeling and Analytics Vendor", "Data Analytics", "Medium", "Limited", "Low", "No", "Medium"),
    ("Cloud Data Warehouse Provider", "Data Warehousing", "Medium", "Direct", "Medium", "No", "Medium"),
    ("E-Signature and Document Workflow Vendor", "Document Management", "Medium", "Limited", "Medium", "No", "Medium"),
    ("Payroll Processing Vendor", "Payroll", "High", "Limited", "Medium", "No", "Medium"),
    ("Contact Center Telephony Provider", "Telephony", "Medium", "Limited", "Medium", "No", "Medium"),
    ("Endpoint Detection and Response Vendor", "Security Tooling", "Medium", "Direct", "Medium", "Yes", "Medium"),
    ("Secrets Management Platform Vendor", "Security Infrastructure", "High", "Direct", "High", "Yes", "High"),
    ("Cloud Monitoring and Observability Vendor", "Monitoring / Observability", "Medium", "Direct", "Medium", "No", "Medium"),
    ("Legal and Compliance Consulting Firm", "Professional Services", "Low", "None", "Low", "No", "Low"),
    ("Translation and Localization Vendor", "Content Services", "Low", "None", "Low", "No", "Low"),
    ("Mobile App Analytics SDK Provider", "Mobile Analytics", "Medium", "Limited", "Medium", "No", "Medium"),
]

vend_rows = []
vnum = next_num(vendors_df, "vendor_id")
for i, spec in enumerate(NEW_VENDORS):
    name, service_type, sensitivity, connectivity, criticality, priv_access, tier = spec
    vend_rows.append({
        "vendor_id": f"VEND-{vnum + i:03d}",
        "vendor_name": name,
        "service_type": service_type,
        "data_sensitivity": sensitivity,
        "connectivity": connectivity,
        "criticality": criticality,
        "privileged_access": priv_access,
        "risk_tier": tier,
    })

vendors_out = pd.concat([vendors_df, pd.DataFrame(vend_rows)], ignore_index=True)
vendors_out.to_csv(DATA_DIR + "vendors.csv", index=False)
print(f"vendors.csv -> {len(vendors_out)} rows")


# ==============================================================================
# 5. VENDOR ASSESSMENTS  (existing -> ~46 total, 1 new cycle per vendor)
# ==============================================================================
va_df = load("vendor_assessment.csv")
if va_df.empty:
    va_df = load("vendor_assessments.csv")

va_rows = []
va_num = next_num(va_df, "assessment_id")
REVIEW_TYPES = ["Onboarding", "Periodic Review", "Targeted Review"]

for _, row in vendors_out.iterrows():
    vid = row["vendor_id"]
    tier = row["risk_tier"]
    n_cycles = 1  # 1 new assessment cycle per vendor
    for c in range(n_cycles):
        days_ago_start = 400
        days_ago_end = 30
        assess_date = rand_date_between(days_ago_start, days_ago_end)
        next_due = assess_date + timedelta(days=365)
        score = random.randint(70, 95) if tier != "High" else random.randint(65, 92)
        findings = 0 if score > 88 else random.randint(0, 4)
        va_rows.append({
            "assessment_id": f"VA-{va_num:03d}",
            "vendor_id": vid,
            "assessment_date": fmt(assess_date),
            "review_type": random.choice(REVIEW_TYPES),
            "security_score": score,
            "open_findings": findings,
            "next_review_due": fmt(next_due),
        })
        va_num += 1

va_out = pd.concat([va_df, pd.DataFrame(va_rows)], ignore_index=True)
va_out.to_csv(DATA_DIR + "vendor_assessment.csv", index=False)
print(f"vendor_assessment.csv -> {len(va_out)} rows")


# ==============================================================================
# 6. POLICY REGISTER  (existing 10 -> 25 total)
# ==============================================================================
policy_df = load("policy_register.csv")
NEW_POLICIES = [
    ("Cryptography and Key Management Policy", "Cloud Infrastructure", "1.0", "Yes"),
    ("Network Security Policy", "Cloud Infrastructure", "1.0", "No"),
    ("Secure Software Development Policy", "Engineering", "1.1", "Yes"),
    ("Mobile Device and BYOD Policy", "IT Operations", "1.0", "Yes"),
    ("Cloud Security and Shared Responsibility Policy", "Cloud Infrastructure", "1.0", "No"),
    ("Data Classification Policy", "Security Compliance", "1.2", "Yes"),
    ("Third-Party Risk Management Policy", "Procurement", "1.1", "No"),
    ("AML and KYC Data Handling Policy", "Legal Privacy", "1.0", "Yes"),
    ("Data Retention and Disposal Policy", "Legal Privacy", "1.1", "Yes"),
    ("Remote Access and Telework Policy", "IT Operations", "1.0", "Yes"),
    ("Secrets and Credential Management Policy", "Cloud Infrastructure", "1.0", "No"),
    ("Physical and Environmental Security Policy", "Business Continuity", "1.0", "No"),
    ("Segregation of Duties Policy", "Security Compliance", "1.0", "No"),
    ("Cross-Border Data Transfer Policy", "Legal Privacy", "1.0", "Yes"),
    ("Vulnerability Disclosure Policy", "Security Compliance", "1.0", "No"),
]

policy_rows = []
pnum = next_num(policy_df, "policy_id")
for i, spec in enumerate(NEW_POLICIES):
    name, owner, version, attest = spec
    last_review = rand_date_between(400, 30)
    next_due = last_review + timedelta(days=365)
    status = "Overdue" if next_due < AS_OF else "Active"
    policy_rows.append({
        "policy_id": f"POL-{pnum + i:03d}",
        "policy_name": name, "owner": owner, "version": version,
        "last_review_date": fmt(last_review), "next_review_due": fmt(next_due),
        "attestation_required": attest, "status": status,
    })

policy_out = pd.concat([policy_df, pd.DataFrame(policy_rows)], ignore_index=True)
policy_out.to_csv(DATA_DIR + "policy_register.csv", index=False)
print(f"policy_register.csv -> {len(policy_out)} rows")


# ==============================================================================
# 7. RISK REGISTER  (existing 10 -> 30 total)
# ==============================================================================
risk_df = load("risk_register.csv")
NEW_RISKS = [
    ("Ransomware attack disrupting core banking availability", "Cyber Security", 3, 5, "Weak", "Security Operations"),
    ("AML transaction monitoring model failing to detect emerging typologies", "Model Risk", 3, 5, "Moderate", "Security Compliance"),
    ("Concentration risk from single cloud infrastructure provider dependency", "Operational", 2, 5, "Moderate", "Cloud Infrastructure"),
    ("Insider misuse of privileged access to customer financial data", "Access Management", 2, 5, "Moderate", "Security Operations"),
    ("Open banking API partner exposing customer data through weak controls", "Third-Party Risk", 3, 4, "Weak", "Security Compliance"),
    ("Mobile banking application vulnerability exploited by attackers", "Application Security", 3, 4, "Moderate", "Engineering"),
    ("Key person dependency in compliance and audit functions", "Operational", 3, 3, "Weak", "Executive Leadership"),
    ("Cross-border data transfer non-compliance with residency commitments", "Privacy", 2, 4, "Moderate", "Legal Privacy"),
    ("Credential stuffing attack against customer digital banking accounts", "Cyber Security", 4, 4, "Moderate", "Security Operations"),
    ("Third-party vendor concentration in payment processing chain", "Third-Party Risk", 2, 5, "Moderate", "Procurement"),
    ("Delayed detection of cloud storage misconfiguration exposing data", "Cloud Security", 3, 4, "Weak", "Cloud Infrastructure"),
    ("Fraud model bias resulting in inequitable customer treatment", "Model Risk", 2, 4, "Moderate", "Security Compliance"),
    ("Regulatory change management gap for new DOJ Data Security Program rules", "Regulatory", 3, 4, "Weak", "Legal Privacy"),
    ("Supply chain attack via compromised open-source dependency", "Application Security", 2, 5, "Weak", "Engineering"),
    ("Business continuity failure during regional cloud outage", "Business Continuity", 2, 5, "Moderate", "Cloud Infrastructure"),
    ("Contractor access not revoked promptly after engagement end", "Access Management", 3, 3, "Weak", "IT Operations"),
    ("Customer data exposure through misconfigured SaaS application", "Cloud Security", 3, 4, "Moderate", "IT Operations"),
    ("Phishing-driven account takeover of employee credentials", "Awareness", 3, 4, "Moderate", "HR"),
    ("Inadequate breach notification readiness across jurisdictions", "Regulatory", 2, 4, "Weak", "Legal Privacy"),
    ("Data quality issues undermining regulatory report accuracy", "Regulatory", 2, 3, "Moderate", "Legal Privacy"),
]

risk_rows = []
rnum = next_num(risk_df, "risk_id")
for i, spec in enumerate(NEW_RISKS):
    title, category, likelihood, impact, strength, owner = spec
    inherent = likelihood * impact
    strength_factor = {"Weak": 0.85, "Moderate": 0.65, "Strong": 0.4}[strength]
    residual = max(round(inherent * strength_factor), 1)
    target_date = AS_OF + timedelta(days=random.randint(30, 240))
    status = random.choice(["Open", "In Progress", "In Progress", "Open"])
    risk_rows.append({
        "risk_id": f"RISK-{rnum + i:03d}",
        "risk_title": title, "category": category, "likelihood": likelihood,
        "impact": impact, "inherent_score": inherent, "control_strength": strength,
        "residual_score": residual,
        "treatment_plan": f"Implement enhanced controls and monitoring to reduce {category.lower()} exposure",
        "owner": owner, "target_date": fmt(target_date), "status": status,
    })

risk_out = pd.concat([risk_df, pd.DataFrame(risk_rows)], ignore_index=True)
risk_out.to_csv(DATA_DIR + "risk_register.csv", index=False)
print(f"risk_register.csv -> {len(risk_out)} rows")


# ==============================================================================
# 8. CORRECTIVE ACTIONS  (existing 8 -> 20 total)
# ==============================================================================
ca_df = load("corrective_actions.csv")
SOURCES = ["Internal Audit", "External Auditor", "Management Review", "Security Incident", "Regulatory Inquiry"]
STATUSES = ["Open", "In Progress", "Pending Validation"]

ca_rows = []
ca_num = next_num(ca_df, "ca_id")
sample_controls = controls_out.sample(n=12, random_state=7)
for i, (_, crow) in enumerate(sample_controls.iterrows()):
    opened = rand_date_between(300, 20)
    target = opened + timedelta(days=random.randint(60, 180))
    status = random.choice(STATUSES)
    ca_rows.append({
        "ca_id": f"CA-{ca_num + i:03d}",
        "source": random.choice(SOURCES),
        "related_item": f"{crow['control_id']} {crow['domain']}",
        "root_cause": f"Process gap identified in {crow['domain'].lower()} operations",
        "owner": crow["owner"],
        "opened_date": fmt(opened),
        "target_date": fmt(target),
        "status": status,
        "effectiveness_review": "Pending validation" if status != "Pending Validation" else "Follow-up review scheduled",
    })

ca_out = pd.concat([ca_df, pd.DataFrame(ca_rows)], ignore_index=True)
ca_out.to_csv(DATA_DIR + "corrective_actions.csv", index=False)
print(f"corrective_actions.csv -> {len(ca_out)} rows")


# ==============================================================================
# 9. PRIVACY REQUESTS  (existing 10 -> 30 total)
# ==============================================================================
pr_df = load("privacy_requests.csv")
REQUEST_TYPES = ["Access", "Correction", "Deletion", "Complaint", "Inquiry"]

pr_rows = []
pr_num = next_num(pr_df, "request_id")
for i in range(20):
    received = rand_date_between(360, 5)
    due = received + timedelta(days=30)
    is_closed = (AS_OF - received).days > random.randint(20, 40)
    status = "Closed" if is_closed else random.choice(["Open", "In Progress"])
    days_open = (AS_OF - received).days if not is_closed else random.randint(15, 40)
    pr_rows.append({
        "request_id": f"PR-{pr_num + i:03d}",
        "request_type": random.choice(REQUEST_TYPES),
        "received_date": fmt(received),
        "due_date": fmt(due),
        "status": status,
        "days_open": days_open,
        "owner": "Legal Privacy",
    })

pr_out = pd.concat([pr_df, pd.DataFrame(pr_rows)], ignore_index=True)
pr_out.to_csv(DATA_DIR + "privacy_requests.csv", index=False)
print(f"privacy_requests.csv -> {len(pr_out)} rows")


# ==============================================================================
# 10. DATA INVENTORY  (existing 10 -> 20 total)
# ==============================================================================
di_df = load("data_inventory.csv")
NEW_DATA_ASSETS = [
    ("KYC Identity Verification System", "Customer identity documents and verification data", "Yes", "Canada", "7 years", "Regulatory KYC compliance", "Legal Privacy"),
    ("AML Screening Platform", "Sanctions screening and AML case data", "Yes", "Canada", "7 years", "AML regulatory compliance", "Legal Privacy"),
    ("Card and Payment Processing System", "Cardholder and payment transaction data", "Yes", "Canada", "7 years", "Payment processing and PCI compliance", "Product Owner - Banking"),
    ("Fraud Detection Platform", "Transaction risk signals and fraud case data", "Yes", "Canada", "3 years", "Fraud prevention", "Security Operations"),
    ("Marketing Consent Management System", "Customer marketing consent and preference records", "Yes", "Canada", "3 years", "Marketing communications compliance", "Marketing"),
    ("Mobile App Telemetry Platform", "Mobile app usage and device telemetry data", "Yes", "Multi-region", "1 year", "Product improvement and diagnostics", "Product Analytics"),
    ("Contact Center Recording System", "Customer call recordings and transcripts", "Yes", "Canada", "2 years", "Quality assurance and dispute resolution", "Customer Support"),
    ("Credit Bureau Data Integration", "Credit bureau inquiry and scoring data", "Yes", "Canada", "7 years", "Credit decisioning", "Product Owner - Banking"),
    ("Open Banking API Gateway", "Third-party partner data access logs", "Yes", "Canada", "3 years", "Open banking partner governance", "Security Compliance"),
    ("Employee Background Check Records", "Pre-employment screening results", "Yes", "Canada", "3 years", "Employment eligibility verification", "HR"),
]

di_rows = []
di_num = next_num(di_df, "asset_id")
for i, spec in enumerate(NEW_DATA_ASSETS):
    system, dtype, pii, residency, retention, purpose, owner = spec
    di_rows.append({
        "asset_id": f"DATA-{di_num + i:03d}",
        "system_name": system, "data_type": dtype, "contains_pii": pii,
        "residency": residency, "retention_period": retention,
        "lawful_purpose": purpose, "owner": owner,
    })

di_out = pd.concat([di_df, pd.DataFrame(di_rows)], ignore_index=True)
di_out.to_csv(DATA_DIR + "data_inventory.csv", index=False)
print(f"data_inventory.csv -> {len(di_out)} rows")

print("\nAll datasets expanded successfully.")