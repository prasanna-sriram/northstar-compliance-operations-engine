"""
policy_review_tracker.py
-------------------------------------------------------------------------------
Purpose: Identify overdue and soon-due policy reviews to support ISO 27001
         policy lifecycle governance (drafting, review, approval, annual
         re-review, and version control).

Reads:  data/policy_register.csv
Writes: outputs/policy_review_status.csv

Classification logic:
    - Overdue:   next_review_due is in the past relative to AS_OF_DATE.
    - Due Soon:  next_review_due falls within the next 30 days.
    - On Track:  next_review_due is more than 30 days away.

Usage:
    python policy_review_tracker.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)
DUE_SOON_WINDOW_DAYS = 30


def classify_review_status(days_until_due: int) -> str:
    """Classify a policy record based on days remaining until next_review_due."""
    if days_until_due < 0:
        return "Overdue"
    elif days_until_due <= DUE_SOON_WINDOW_DAYS:
        return "Due Soon"
    else:
        return "On Track"


def track_policy_reviews(policy_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Compute review status and days_until_due for every policy record."""
    df = policy_df.copy()
    df["next_review_due"] = pd.to_datetime(df["next_review_due"])
    df["last_review_date"] = pd.to_datetime(df["last_review_date"])
    df["days_until_due"] = (df["next_review_due"] - as_of).dt.days
    df["review_status"] = df["days_until_due"].apply(classify_review_status)
    return df


def main():
    policies = pd.read_csv(DATA_DIR + "policy_register.csv")
    tracked = track_policy_reviews(policies, AS_OF_DATE)

    report = tracked[[
        "policy_id", "policy_name", "owner", "version",
        "last_review_date", "next_review_due", "days_until_due",
        "attestation_required", "review_status",
    ]].sort_values("days_until_due")

    report.to_csv(OUTPUT_DIR + "policy_review_status.csv", index=False)

    print(
        f"Policy review tracking complete: "
        f"{(tracked['review_status'] == 'Overdue').sum()} overdue, "
        f"{(tracked['review_status'] == 'Due Soon').sum()} due soon."
    )


if __name__ == "__main__":
    main()