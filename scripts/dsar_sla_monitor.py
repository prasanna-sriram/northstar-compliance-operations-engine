"""
dsar_sla_monitor.py
-------------------------------------------------------------------------------
Purpose: Compute PIPEDA-aligned SLA status for open privacy requests (DSARs)
         to support timely response tracking and privacy operations reporting.

Reads:  data/privacy_requests.csv
Writes: outputs/dsar_status_report.csv

Classification logic (for non-Closed requests only):
    - Past Due:  due_date is in the past relative to AS_OF_DATE.
    - Due Soon:  due_date falls within the next 7 days.
    - On Track:  due_date is more than 7 days away.

Usage:
    python dsar_sla_monitor.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)
DUE_SOON_WINDOW_DAYS = 7


def classify_sla_status(days_until_due: int) -> str:
    """Classify a privacy request based on days remaining until due_date."""
    if days_until_due < 0:
        return "Past Due"
    elif days_until_due <= DUE_SOON_WINDOW_DAYS:
        return "Due Soon"
    else:
        return "On Track"


def monitor_dsar_sla(pr_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Compute SLA status and days_until_due for every open privacy request."""
    df = pr_df.copy()
    df["due_date"] = pd.to_datetime(df["due_date"])
    df["received_date"] = pd.to_datetime(df["received_date"])
    active = df[df["status"] != "Closed"].copy()
    active["days_until_due"] = (active["due_date"] - as_of).dt.days
    active["sla_status"] = active["days_until_due"].apply(classify_sla_status)
    return active


def main():
    privacy_requests = pd.read_csv(DATA_DIR + "privacy_requests.csv")
    monitored = monitor_dsar_sla(privacy_requests, AS_OF_DATE)

    report = monitored[[
        "request_id", "request_type", "received_date", "due_date",
        "status", "days_open", "owner", "days_until_due", "sla_status",
    ]].sort_values("days_until_due")

    report.to_csv(OUTPUT_DIR + "dsar_status_report.csv", index=False)

    print(
        f"DSAR SLA monitor complete: "
        f"{(monitored['sla_status'] == 'Past Due').sum()} past due, "
        f"{(monitored['sla_status'] == 'Due Soon').sum()} due soon."
    )


if __name__ == "__main__":
    main()