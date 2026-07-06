from __future__ import annotations

import pandas as pd


DEFAULT_WEIGHTS = {
    "ranking": 0.30,
    "placement": 0.30,
    "fees": 0.20,
    "admission_fit": 0.20,
}


def _ascending_score(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().sum() == 0:
        return pd.Series(0.5, index=series.index)

    minimum = numeric.min()
    maximum = numeric.max()
    if minimum == maximum:
        return pd.Series(1.0, index=series.index)
    return 1 - ((numeric - minimum) / (maximum - minimum)).fillna(1)


def _descending_score(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().sum() == 0:
        return pd.Series(0.5, index=series.index)

    minimum = numeric.min()
    maximum = numeric.max()
    if minimum == maximum:
        return pd.Series(1.0, index=series.index)
    return ((numeric - minimum) / (maximum - minimum)).fillna(0)


def rank_recommendations(
    frame: pd.DataFrame,
    student_rank: int | None = None,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    if frame.empty:
        return frame.assign(recommendation_score=[])

    active_weights = DEFAULT_WEIGHTS | (weights or {})
    ranked = frame.copy()

    ranked["ranking_score"] = _ascending_score(ranked["nirf_rank"])
    ranked["placement_score"] = _descending_score(ranked["average_package_lpa"])
    ranked["fees_score"] = _ascending_score(ranked["total_fees"])

    if student_rank is not None and "closing_rank" in ranked:
        closing_rank = pd.to_numeric(ranked["closing_rank"], errors="coerce")
        gap = (closing_rank - student_rank).clip(lower=0)
        ranked["admission_fit_score"] = _ascending_score(gap)
        ranked.loc[closing_rank.isna(), "admission_fit_score"] = 0.5
    else:
        ranked["admission_fit_score"] = 0.5

    ranked["recommendation_score"] = (
        active_weights["ranking"] * ranked["ranking_score"]
        + active_weights["placement"] * ranked["placement_score"]
        + active_weights["fees"] * ranked["fees_score"]
        + active_weights["admission_fit"] * ranked["admission_fit_score"]
    )

    return ranked.sort_values(
        by=["recommendation_score", "nirf_rank", "average_package_lpa"],
        ascending=[False, True, False],
        na_position="last",
    )
