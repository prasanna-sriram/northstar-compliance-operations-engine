"""
risk_scoring_engine.py
-------------------------------------------------------------------------------
Purpose: Turn the static risk register into a working prioritization engine.
         Computes treatment urgency, flags overdue treatments, and ranks
         risks for executive review, supporting ISO 27001's requirement for
         a defined risk assessment and treatment process with documented,
         actionable outputs (not just a stored register).

Reads:  data/risk_register.csv
Writes: outputs/risk_summary.csv

Scoring logic:
    - risk_level: derived from residual_score.
        >= 15  -> Critical
        >= 10  -> High
        >= 5   -> Medium
        <  5   -> Low
    - days_to_target: days remaining until target_date (negative = overdue).
    - treatment_overdue: True if target_date has passed and status != Closed.
    - treatment_urgency_score: residual_score, boosted by +5 if the
      treatment is overdue. This is the primary ranking field for
      executive review — it prioritizes severity AND lateness together.
    - executive_attention_flag: True if the risk is Critical, OR if it is
      High/Critical AND overdue on treatment. This isolates the small set
      of risks that genuinely need leadership visibility.
    - exec_rank: 1-based rank by treatment_urgency_score, descending.

Usage:
    python risk_scoring_engine.py
-------------------------------------------------------------------------------
"""

import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
AS_OF_DATE = datetime(2026, 7, 24)

RISK_LEVEL_THRESHOLDS = [
    (15, "Critical"),
    (10, "High"),
    (5, "Medium"),
    (0, "Low"),
]
OVERDUE_URGENCY_BOOST = 5


def classify_risk_level(residual_score: int) -> str:
    """Map a residual score to a categorical risk level."""
    for threshold, label in RISK_LEVEL_THRESHOLDS:
        if residual_score >= threshold:
            return label
    return "Low"


def compute_treatment_urgency(residual_score: int, treatment_overdue: bool) -> int:
    """Boost urgency score for risks whose treatment plan has missed its target date."""
    return residual_score + (OVERDUE_URGENCY_BOOST if treatment_overdue else 0)


def score_risks(risk_df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Apply risk level classification, overdue detection, and urgency ranking."""
    df = risk_df.copy()
    df["target_date"] = pd.to_datetime(df["target_date"])

    df["days_to_target"] = (df["target_date"] - as_of).dt.days
    df["treatment_overdue"] = (df["days_to_target"] < 0) & (df["status"] != "Closed")

    df["risk_level"] = df["residual_score"].apply(classify_risk_level)

    df["treatment_urgency_score"] = df.apply(
        lambda row: compute_treatment_urgency(row["residual_score"], row["treatment_overdue"]),
        axis=1,
    )

    df["executive_attention_flag"] = (
        (df["risk_level"] == "Critical")
        | ((df["risk_level"] == "High") & df["treatment_overdue"])
    )

    df = df.sort_values("treatment_urgency_score", ascending=False).reset_index(drop=True)
    df["exec_rank"] = df.index + 1

    return df


def main():
    risks = pd.read_csv(DATA_DIR + "risk_register.csv")
    scored = score_risks(risks, AS_OF_DATE)

    report = scored[[
        "exec_rank", "risk_id", "risk_title", "category", "likelihood", "impact",
        "inherent_score", "control_strength", "residual_score", "risk_level",
        "treatment_plan", "owner", "target_date", "days_to_target",
        "treatment_overdue", "treatment_urgency_score",
        "executive_attention_flag", "status",
    ]]

    report.to_csv(OUTPUT_DIR + "risk_summary.csv", index=False)

    print(
        f"Risk scoring complete: {len(scored)} risks scored. "
        f"{scored['executive_attention_flag'].sum()} flagged for executive attention. "
        f"{scored['treatment_overdue'].sum()} treatments overdue."
    )


if __name__ == "__main__":
    main()