"""
vendor_tiering.py
-------------------------------------------------------------------------------
Purpose: Compute a weighted composite risk score for every vendor and derive
         a risk tier (High/Medium/Low), flag vendors overdue for reassessment
         against their tier's required cadence, and surface vendors with open
         critical findings that need remediation follow-up. Supports SOC 2's
         expectation of a documented vendor classification and review process,
         and ISO 27001's supplier relationship security requirements.

Reads:  data/vendors.csv, data/vendor_assessment.csv
Writes: outputs/vendor_risk_summary.csv

Scoring methodology (weighted composite, 0-100 scale):
    - data_sensitivity   (weight 30%): High=4, Medium=2, Low=1
    - business_criticality (weight 30%): High=4, Medium=2, Low=1
    - connectivity        (weight 20%): Direct=3, Limited=2, None=0
    - privileged_access   (weight 20%): Yes=3, No=0

    Each factor is normalized to its own maximum before weighting, so the
    composite score always falls between 0 and 100.

Tier thresholds:
    - High:   composite_risk_score >= 70
    - Medium: composite_risk_score >= 40
    - Low:    composite_risk_score <  40

Reassessment cadence by tier (days):
    - High:   365  (annual)
    - Medium: 540  (~18 months)
    - Low:    730  (24 months)

high_priority_flag logic:
    True if the vendor is High tier AND either its reassessment is overdue
    OR it currently has open findings from its last assessment. This isolates
    the small set of vendors that need immediate attention rather than every
    High-tier vendor by default.

Usage:
    python vendor_tiering.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)

FACTOR_SCALES = {
    "data_sensitivity": {"High": 4, "Medium": 2, "Low": 1},
    "criticality": {"High": 4, "Medium": 2, "Low": 1},
    "connectivity": {"Direct": 3, "Limited": 2, "None": 0},
    "privileged_access": {"Yes": 3, "No": 0},
}
FACTOR_WEIGHTS = {
    "data_sensitivity": 0.30,
    "criticality": 0.30,
    "connectivity": 0.20,
    "privileged_access": 0.20,
}

TIER_THRESHOLDS = [(70, "High"), (40, "Medium"), (0, "Low")]
REASSESSMENT_CADENCE_DAYS = {"High": 365, "Medium": 540, "Low": 730}


def compute_composite_score(row: pd.Series) -> float:
    """Compute a normalized, weighted 0-100 composite risk score for one vendor."""
    score = 0.0
    for factor, weight in FACTOR_WEIGHTS.items():
        scale = FACTOR_SCALES[factor]
        raw_value = scale.get(row[factor], 0)
        max_value = max(scale.values())
        score += (raw_value / max_value) * weight * 100
    return round(score, 1)


def classify_tier(score: float) -> str:
    """Map a composite risk score to a High/Medium/Low tier."""
    for threshold, label in TIER_THRESHOLDS:
        if score >= threshold:
            return label
    return "Low"


def score_vendors(vendors_df: pd.DataFrame) -> pd.DataFrame:
    """Compute composite score and calculated tier for every vendor."""
    df = vendors_df.copy()
    df["composite_risk_score"] = df.apply(compute_composite_score, axis=1)
    df["calculated_tier"] = df["composite_risk_score"].apply(classify_tier)
    return df


def attach_assessment_status(scored_df: pd.DataFrame, assessments_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Attach latest assessment info and compute reassessment-due status."""
    latest = (
        assessments_df.sort_values("assessment_date")
        .groupby("vendor_id")
        .tail(1)[["vendor_id", "assessment_date", "next_review_due", "security_score", "open_findings"]]
    )

    merged = scored_df.merge(latest, on="vendor_id", how="left")
    merged["next_review_due"] = pd.to_datetime(merged["next_review_due"])
    merged["days_until_reassessment"] = (merged["next_review_due"] - as_of).dt.days
    merged["reassessment_overdue"] = merged["days_until_reassessment"] < 0
    merged["open_findings"] = merged["open_findings"].fillna(0).astype(int)

    merged["high_priority_flag"] = (
        (merged["calculated_tier"] == "High")
        & (merged["reassessment_overdue"] | (merged["open_findings"] > 0))
    )

    return merged


def main():
    vendors = pd.read_csv(DATA_DIR + "vendors.csv")
    assessments = pd.read_csv(DATA_DIR + "vendor_assessment.csv")

    scored = score_vendors(vendors)
    result = attach_assessment_status(scored, assessments, AS_OF_DATE)

    result = result.sort_values(
        ["high_priority_flag", "composite_risk_score"], ascending=[False, False]
    )

    report = result[[
        "vendor_id", "vendor_name", "service_type", "data_sensitivity",
        "connectivity", "criticality", "privileged_access",
        "composite_risk_score", "calculated_tier", "risk_tier",
        "assessment_date", "next_review_due", "days_until_reassessment",
        "reassessment_overdue", "open_findings", "high_priority_flag",
    ]]

    report.to_csv(OUTPUT_DIR + "vendor_risk_summary.csv", index=False)

    print(
        f"Vendor tiering complete: {len(report)} vendors scored. "
        f"{(report['calculated_tier'] == 'High').sum()} High tier, "
        f"{report['reassessment_overdue'].sum()} overdue for reassessment, "
        f"{report['high_priority_flag'].sum()} flagged high priority."
    )


if __name__ == "__main__":
    main()