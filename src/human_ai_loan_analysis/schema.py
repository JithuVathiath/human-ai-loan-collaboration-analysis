"""Schema checks for public or synthetic decision data."""

from __future__ import annotations

import pandas as pd

REQUIRED_DECISION_COLUMNS = {
    "participant_id",
    "applicant_id",
    "initial_decision",
    "ai_decision",
    "final_decision",
    "outcome",
    "group",
}


def validate_decision_frame(frame: pd.DataFrame) -> None:
    """Raise a clear error when a decision frame violates the public schema."""
    missing = REQUIRED_DECISION_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("decision frame must not be empty")
    if frame[["participant_id", "applicant_id"]].isna().any().any():
        raise ValueError("participant_id and applicant_id must not be missing")

    for column in ("initial_decision", "ai_decision", "final_decision", "outcome"):
        observed = frame[column].dropna()
        if not observed.isin([0, 1, False, True]).all():
            raise ValueError(f"{column} must contain only binary values or missing values")

