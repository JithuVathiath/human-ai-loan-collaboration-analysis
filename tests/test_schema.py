import pandas as pd
import pytest

from human_ai_loan_analysis.schema import validate_decision_frame


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "participant_id": ["p01", "p01"],
            "applicant_id": ["a01", "a02"],
            "initial_decision": [0, 1],
            "ai_decision": [1, 1],
            "final_decision": [1, 1],
            "outcome": [1, 0],
            "group": ["Orange", "Purple"],
        }
    )


def test_valid_frame_passes() -> None:
    validate_decision_frame(valid_frame())


def test_missing_column_raises() -> None:
    frame = valid_frame().drop(columns="group")
    with pytest.raises(ValueError, match="missing required columns"):
        validate_decision_frame(frame)


def test_non_binary_decision_raises() -> None:
    frame = valid_frame()
    frame.loc[0, "ai_decision"] = 3
    with pytest.raises(ValueError, match="ai_decision"):
        validate_decision_frame(frame)

