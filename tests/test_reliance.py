import numpy as np
import pytest

from human_ai_loan_analysis.reliance import (
    RELIANCE_CATEGORIES,
    classify_reliance,
    reliance_summary,
    signed_group_gap,
)


def test_all_reliance_categories_and_non_identifiable_cases() -> None:
    result = classify_reliance(
        initial_decision=[0, 1, 1, 0, 1, 0],
        ai_decision=[1, 0, 0, 1, 1, 1],
        final_decision=[1, 1, 0, 0, 1, np.nan],
        outcome=[1, 1, 1, 1, 1, 1],
    )

    assert result.tolist() == [
        "Appropriate acceptance",
        "Appropriate resistance",
        "Overreliance",
        "Underreliance",
        None,
        "Unresolved",
    ]


def test_reliance_summary_reports_both_denominators() -> None:
    categories = [*RELIANCE_CATEGORIES, "Unresolved", None]
    summary = reliance_summary(categories).set_index("category")

    assert summary.loc["Appropriate acceptance", "share_of_initial_disagreements"] == pytest.approx(
        0.2
    )
    resolved_share = summary.loc[
        "Appropriate acceptance", "share_of_resolved_disagreements"
    ]
    assert resolved_share == pytest.approx(0.25)
    assert np.isnan(summary.loc["Unresolved", "share_of_resolved_disagreements"])


def test_signed_group_gap_has_explicit_direction() -> None:
    gap = signed_group_gap(
        values=[0, 1, 1, 1],
        groups=["Orange", "Orange", "Purple", "Purple"],
        comparison_group="Purple",
        reference_group="Orange",
    )

    assert gap == pytest.approx(0.5)


def test_invalid_binary_value_raises() -> None:
    with pytest.raises(ValueError):
        classify_reliance([0], [2], [1], [1])
