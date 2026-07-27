"""
control_effectiveness_summary.py
-------------------------------------------------------------------------------
Purpose: Summarize control test pass/fail rates by domain and owner to
         support internal audit trend analysis and management review
         inputs on recurring control weaknesses.

Reads:  data/control_tests.csv, data/controls.csv
Writes: outputs/control_effectiveness_summary.csv

Logic:
    - Join test results to controls to attach domain and owner context.
    - Pivot test results into Pass / Pass with Observation / Fail counts.
    - Compute a pass_rate_pct per domain/owner combination for trend
      analysis and dashboard use.

Usage:
    python control_effectiveness_summary.py
-------------------------------------------------------------------------------
"""

import pandas as pd

DATA_DIR = "data/"
OUTPUT_DIR = "outputs/"
RESULT_CATEGORIES = ["Pass", "Pass with Observation", "Fail"]


def summarize_control_effectiveness(tests_df: pd.DataFrame, controls_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot control test results by domain and owner, computing pass rate."""
    merged = tests_df.merge(
        controls_df[["control_id", "domain", "owner"]],
        on="control_id", how="left",
    )

    counts = merged.groupby(["domain", "owner", "result"]).size().reset_index(name="count")
    pivot = counts.pivot_table(
        index=["domain", "owner"], columns="result", values="count", fill_value=0
    ).reset_index()

    for category in RESULT_CATEGORIES:
        if category not in pivot.columns:
            pivot[category] = 0

    pivot["total_tests"] = pivot[RESULT_CATEGORIES].sum(axis=1)
    pivot["pass_rate_pct"] = (pivot["Pass"] / pivot["total_tests"] * 100).round(1)

    return pivot.sort_values("pass_rate_pct")


def main():
    control_tests = pd.read_csv(DATA_DIR + "control_tests.csv")
    controls = pd.read_csv(DATA_DIR + "controls.csv")

    summary = summarize_control_effectiveness(control_tests, controls)
    summary.to_csv(OUTPUT_DIR + "control_effectiveness_summary.csv", index=False)

    weak_domains = summary[summary["pass_rate_pct"] < 80]["domain"].tolist()
    print(
        f"Control effectiveness summary complete: {len(summary)} domain/owner "
        f"groups analyzed. Domains below 80% pass rate: {weak_domains}"
    )


if __name__ == "__main__":
    main()