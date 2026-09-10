"""Deterministic metrics for human-AI disagreement and reliance.

These functions contain no participant data and make no causal or fairness
claims. A binary value of 1 represents the caller's documented positive
decision or outcome; the package does not assign approval semantics itself.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

RELIANCE_CATEGORIES = (
    "Appropriate acceptance",
    "Appropriate resistance",
    "Overreliance",
    "Underreliance",
)


def _binary_or_missing(values: Iterable[object], *, name: str) -> np.ndarray:
    result = np.asarray(list(values), dtype=object)
    if result.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    observed = result[~pd.isna(result)]
    if not np.isin(observed, [0, 1, False, True]).all():
        raise ValueError(f"{name} must contain only binary values or missing values")
    return result


def classify_reliance(
    initial_decision: Iterable[object],
    ai_decision: Iterable[object],
    final_decision: Iterable[object],
    outcome: Iterable[object],
) -> pd.Series:
    """Classify reliance for initial human-AI disagreements.

    Initial-agreement cases return ``None`` because the observed final choice
    cannot identify acceptance or resistance. Missing final decisions in an
    initial-disagreement case return ``Unresolved``.
    """
    initial = _binary_or_missing(initial_decision, name="initial_decision")
    computer = _binary_or_missing(ai_decision, name="ai_decision")
    final = _binary_or_missing(final_decision, name="final_decision")
    observed_outcome = _binary_or_missing(outcome, name="outcome")

    lengths = {len(initial), len(computer), len(final), len(observed_outcome)}
    if len(lengths) != 1:
        raise ValueError("all decision inputs must have equal length")

    categories: list[str | None] = []
    for human_value, ai_value, final_value, outcome_value in zip(
        initial, computer, final, observed_outcome, strict=True
    ):
        if pd.isna(human_value) or pd.isna(ai_value) or pd.isna(outcome_value):
            categories.append(None)
            continue
        if human_value == ai_value:
            categories.append(None)
            continue
        if pd.isna(final_value):
            categories.append("Unresolved")
            continue

        ai_correct = ai_value == outcome_value
        followed_ai = final_value == ai_value
        if ai_correct and followed_ai:
            categories.append("Appropriate acceptance")
        elif not ai_correct and not followed_ai:
            categories.append("Appropriate resistance")
        elif not ai_correct and followed_ai:
            categories.append("Overreliance")
        else:
            categories.append("Underreliance")

    return pd.Series(categories, dtype="object", name="reliance_category")


def reliance_summary(categories: Iterable[object]) -> pd.DataFrame:
    """Summarise reliance counts with explicit resolved and total denominators."""
    values = pd.Series(list(categories), dtype="object")
    disagreement_values = values.dropna()
    invalid = set(disagreement_values.unique()) - {*RELIANCE_CATEGORIES, "Unresolved"}
    if invalid:
        raise ValueError(f"unknown reliance categories: {sorted(map(str, invalid))}")

    total_disagreements = int(len(disagreement_values))
    resolved = disagreement_values[disagreement_values != "Unresolved"]
    resolved_count = int(len(resolved))
    rows = []
    for category in (*RELIANCE_CATEGORIES, "Unresolved"):
        count = int((disagreement_values == category).sum())
        rows.append(
            {
                "category": category,
                "count": count,
                "share_of_initial_disagreements": (
                    count / total_disagreements if total_disagreements else np.nan
                ),
                "share_of_resolved_disagreements": (
                    count / resolved_count
                    if resolved_count and category != "Unresolved"
                    else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


def signed_group_gap(
    values: Iterable[float],
    groups: Iterable[object],
    *,
    comparison_group: object,
    reference_group: object,
) -> float:
    """Return comparison-group mean minus reference-group mean."""
    numeric_values = np.asarray(list(values), dtype=float)
    group_values = np.asarray(list(groups), dtype=object)
    if numeric_values.ndim != 1 or group_values.ndim != 1:
        raise ValueError("values and groups must be one-dimensional")
    if len(numeric_values) != len(group_values):
        raise ValueError("values and groups must have equal length")

    comparison = numeric_values[group_values == comparison_group]
    reference = numeric_values[group_values == reference_group]
    comparison = comparison[np.isfinite(comparison)]
    reference = reference[np.isfinite(reference)]
    if not len(comparison) or not len(reference):
        raise ValueError("both requested groups must contain an observed numeric value")
    return float(comparison.mean() - reference.mean())

