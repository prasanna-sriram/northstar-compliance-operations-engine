"""
enhance_privacy_requests.py
-------------------------------------------------------------------------------
Purpose: Enhance the existing privacy_requests.csv with additional fields
         required to support a realistic PIPEDA-aligned DSAR workflow, per
         the Day 7 operating procedure defined in docs/dsar-operating-procedure.md.

Reads:  data/privacy_requests.csv
Writes: data/privacy_requests.csv (overwritten in place with new columns added)

New fields added:
    - identity_verification_status: Verified / Pending / Failed
    - data_sources_searched: comma-separated list of systems searched to
      fulfill the request
    - retention_rule_applied: the retention period/rule governing the
      underlying personal data, mapped by request type
    - residency: data residency location relevant to the request
    - lawful_purpose: the business/legal basis for holding the underlying
      data, mapped by request type

This is a one-time enhancement script — existing row count and IDs are
preserved; only new columns are added.

Usage:
    python enhance_privacy_requests.py
-------------------------------------------------------------------------------
"""

import pandas as pd
import random

random.seed(42)
DATA_DIR = "data/"

IDENTITY_STATUS_WEIGHTS = [("Verified", 0.85), ("Pending", 0.10), ("Failed", 0.05)]

DATA_SOURCE_OPTIONS = [
    "Core Banking Platform, Identity Provider, CRM",
    "Core Banking Platform, HRIS",
    "Marketing Platform, CRM",
    "Core Banking Platform, Fraud Detection Platform, Identity Provider",
    "HRIS, Payroll Processing Vendor",
    "Core Banking Platform, Credit Bureau Data Integration",
    "Contact Center Recording System, CRM",
]

RETENTION_RULES_BY_TYPE = {
    "Access": "7 years (regulatory KYC/AML retention)",
    "Correction": "Active account retention (ongoing)",
    "Deletion": "Subject to 7-year regulatory hold where applicable",
    "Complaint": "3 years (dispute resolution retention)",
    "Inquiry": "1 year (general inquiry log retention)",
}

LAWFUL_PURPOSE_BY_TYPE = {
    "Access": "Provision of banking services and regulatory compliance",
    "Correction": "Maintaining accuracy of customer records for service delivery",
    "Deletion": "Evaluated against regulatory retention obligations before erasure",
    "Complaint": "Dispute resolution and service quality management",
    "Inquiry": "Customer service and privacy accountability",
}


def weighted_choice(weights):
    """Select a label from a list of (label, weight) tuples."""
    r = random.random()
    cumulative = 0.0
    for label, weight in weights:
        cumulative += weight
        if r <= cumulative:
            return label
    return weights[-1][0]


def enhance_privacy_requests(df: pd.DataFrame) -> pd.DataFrame:
    """Add identity verification, data source, retention, and purpose fields."""
    df = df.copy()
    df["identity_verification_status"] = [
        weighted_choice(IDENTITY_STATUS_WEIGHTS) for _ in range(len(df))
    ]
    df["data_sources_searched"] = [
        random.choice(DATA_SOURCE_OPTIONS) for _ in range(len(df))
    ]
    df["retention_rule_applied"] = df["request_type"].map(RETENTION_RULES_BY_TYPE)
    df["residency"] = "Canada"
    df["lawful_purpose"] = df["request_type"].map(LAWFUL_PURPOSE_BY_TYPE)
    return df


def main():
    privacy_requests = pd.read_csv(DATA_DIR + "privacy_requests.csv")
    enhanced = enhance_privacy_requests(privacy_requests)
    enhanced.to_csv(DATA_DIR + "privacy_requests.csv", index=False)
    print(
        f"privacy_requests.csv enhanced -> {len(enhanced)} rows, "
        f"{len(enhanced.columns)} columns "
        f"(added: identity_verification_status, data_sources_searched, "
        f"retention_rule_applied, residency, lawful_purpose)"
    )


if __name__ == "__main__":
    main()