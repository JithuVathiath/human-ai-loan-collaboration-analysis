"""Demonstrate public reliance utilities using synthetic decisions only."""

from __future__ import annotations

import pandas as pd

from human_ai_loan_analysis import classify_reliance, reliance_summary, validate_decision_frame


def main() -> None:
    decisions = pd.DataFrame(
        {
            "participant_id": ["demo_1", "demo_1", "demo_2", "demo_2"],
            "applicant_id": ["case_1", "case_2", "case_3", "case_4"],
            "initial_decision": [0, 1, 1, 0],
            "ai_decision": [1, 0, 0, 1],
            "final_decision": [1, 1, 0, 0],
            "outcome": [1, 1, 1, 1],
            "group": ["Group A", "Group A", "Group B", "Group B"],
        }
    )
    validate_decision_frame(decisions)
    decisions["reliance_category"] = classify_reliance(
        decisions["initial_decision"],
        decisions["ai_decision"],
        decisions["final_decision"],
        decisions["outcome"],
    )

    print("Synthetic demonstration only - these are not study data or findings")
    print(decisions.to_string(index=False))
    print(reliance_summary(decisions["reliance_category"]).to_string(index=False))


if __name__ == "__main__":
    main()

