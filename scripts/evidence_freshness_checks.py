"""
evidence_freshness_check.py
-------------------------------------------------------------------------------
Purpose: Flag missing, stale, and upcoming-due evidence across all controls.
         Supports SOC 2 Type II continuous monitoring and ISO 27001 audit
         readiness by surfacing evidence that needs owner attention.

Reads:  data/controls.csv, data/evidence_inventory.csv
Writes: outputs/overdue_evidence_report.csv

Classification logic:
    - Stale:     next_due_date is in the past relative to AS_OF_DATE.
    - Due Soon:  next_due_date falls within the next 14 days.
    - Current:   next_due_date is more than 14 days away.
    - Missing:   a control has zero evidence records at all (no artifact
                 has ever been logged against it).

Usage:
    python evidence_freshness_check.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)  # update to current date at run time
DUE_SOON_WINDOW_DAYS = 14


def classify_freshness(days_until_due: int) -> str:
    """Classify an evidence record based on days remaining until next_due_date."""
    if days_until_due < 0:
        return "Stale"
    elif days_until_due <= DUE_SOON_WINDOW_DAYS:
        return "Due Soon"
    else:
        return "Current"


def check_evidence_freshness(evidence_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Compute freshness status and days_until_due for every evidence record."""
    df = evidence_df.copy()
    df["next_due_date"] = pd.to_datetime(df["next_due_date"])
    df["last_collected_date"] = pd.to_datetime(df["last_collected_date"])
    df["days_until_due"] = (df["next_due_date"] - as_of).dt.days
    df["freshness_status"] = df["days_until_due"].apply(classify_freshness)
    return df


def find_missing_evidence(controls_df: pd.DataFrame, evidence_df: pd.DataFrame) -> pd.DataFrame:
    """Identify controls with zero evidence records on file."""
    merged = controls_df.merge(
        evidence_df[["control_id", "evidence_id"]],
        on="control_id", how="left",
    )
    missing = merged[merged["evidence_id"].isna()][
        ["control_id", "control_name", "domain", "owner", "evidence_required"]
    ].copy()
    missing["freshness_status"] = "Missing"
    return missing


def main():
    controls = pd.read_csv(DATA_DIR + "controls.csv")
    evidence = pd.read_csv(DATA_DIR + "evidence_inventory.csv")

    freshness = check_evidence_freshness(evidence, AS_OF_DATE)
    missing = find_missing_evidence(controls, evidence)

    report = freshness[freshness["freshness_status"].isin(["Stale", "Due Soon"])]
    report = report[[
        "evidence_id", "control_id", "evidence_name", "source_system",
        "owner", "last_collected_date", "next_due_date",
        "days_until_due", "freshness_status",
    ]]

    report.to_csv(OUTPUT_DIR + "overdue_evidence_report.csv", index=False)

    # One-line status summary for README / daily log notes
    print(
        f"Evidence freshness check complete: "
        f"{(freshness['freshness_status'] == 'Stale').sum()} stale, "
        f"{(freshness['freshness_status'] == 'Due Soon').sum()} due soon, "
        f"{len(missing)} controls missing evidence entirely."
    )


if __name__ == "__main__":
    main()