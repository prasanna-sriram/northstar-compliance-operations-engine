"""
remediation_tracker.py
-------------------------------------------------------------------------------
Purpose: Compute aging buckets for open corrective actions to support ISO
         27001 corrective action tracking and management review reporting.

Reads:  data/corrective_actions.csv
Writes: outputs/remediation_aging_report.csv

Aging bucket logic (based on days past target_date, for non-Closed items):
    - Not Yet Due:  target_date has not yet passed.
    - 0-30:         0 to 30 days overdue.
    - 31-60:        31 to 60 days overdue.
    - 61-90:        61 to 90 days overdue.
    - 90+:          more than 90 days overdue.

Usage:
    python remediation_tracker.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)


def bucket_days_overdue(days_overdue: int) -> str:
    """Assign an aging bucket label based on days overdue."""
    if days_overdue < 0:
        return "Not Yet Due"
    elif days_overdue <= 30:
        return "0-30"
    elif days_overdue <= 60:
        return "31-60"
    elif days_overdue <= 90:
        return "61-90"
    else:
        return "90+"


def track_remediation_aging(ca_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Compute aging bucket for every open (non-Closed) corrective action."""
    df = ca_df.copy()
    df["target_date"] = pd.to_datetime(df["target_date"])
    df["opened_date"] = pd.to_datetime(df["opened_date"])
    open_items = df[df["status"] != "Closed"].copy()
    open_items["days_overdue"] = (as_of - open_items["target_date"]).dt.days
    open_items["aging_bucket"] = open_items["days_overdue"].apply(bucket_days_overdue)
    return open_items


def main():
    corrective_actions = pd.read_csv(DATA_DIR + "corrective_actions.csv")
    aging = track_remediation_aging(corrective_actions, AS_OF_DATE)

    report = aging[[
        "ca_id", "source", "related_item", "owner",
        "opened_date", "target_date", "days_overdue",
        "aging_bucket", "status", "effectiveness_review",
    ]].sort_values("days_overdue", ascending=False)

    report.to_csv(OUTPUT_DIR + "remediation_aging_report.csv", index=False)

    bucket_counts = aging["aging_bucket"].value_counts().to_dict()
    print(f"Remediation aging report complete: {bucket_counts}")


if __name__ == "__main__":
    main()