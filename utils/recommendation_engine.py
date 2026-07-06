from __future__ import annotations

import math
from typing import Any

import pandas as pd

from utils.bigquery_config import BigQueryConfig
from utils.data_loader import load_datasets, to_pandas
from utils.ranking import rank_recommendations


class RecommendationEngine:
    def __init__(self, config: BigQueryConfig | None = None, **_legacy_options: Any):
        bundle = load_datasets(config=config)
        self.backend = bundle.backend
        self.colleges = to_pandas(bundle.colleges)
        self.courses = to_pandas(bundle.courses)
        self.placements = to_pandas(bundle.placements)
        self.cutoffs = to_pandas(bundle.cutoffs)
        self.dataset = self._prepare_dataset()

    def _prepare_dataset(self) -> pd.DataFrame:
        placements = (
            self.placements
            .drop_duplicates(subset=["college_id", "course_name"])
            .copy()
        )

        cutoffs = self.cutoffs.copy()
        cutoffs["year"] = pd.to_numeric(cutoffs["year"], errors="coerce")

        dataset = self.courses.merge(self.colleges, on="college_id", how="left")
        dataset = dataset.merge(placements, on=["college_id", "course_name"], how="left")
        dataset = dataset.merge(
            cutoffs,
            left_on=["college_id", "specialization"],
            right_on=["college_id", "course"],
            how="left",
        )

        numeric_columns = [
            "nirf_rank",
            "total_fees",
            "annual_fees",
            "average_package_lpa",
            "median_package_lpa",
            "highest_package_lpa",
            "placement_percentage",
            "closing_rank",
            "year",
        ]
        for column in numeric_columns:
            if column in dataset:
                dataset[column] = pd.to_numeric(dataset[column], errors="coerce")

        return dataset

    def recommend(
        self,
        state=None,
        city=None,
        ownership=None,
        course_name=None,
        specialization=None,
        exam=None,
        category=None,
        max_total_fees=None,
        min_package=None,
        max_rank=None,
        limit=10,
    ):
        df = self.dataset.copy()

        if state:
            df = df[df["state"].str.lower() == state.lower()]

        if city:
            df = df[df["city"].str.lower() == city.lower()]

        if ownership:
            df = df[df["ownership"].str.lower() == ownership.lower()]

        if course_name:
            df = df[df["course_name"].str.lower() == course_name.lower()]

        if specialization:
            df = df[
                df["specialization"]
                .str.contains(specialization, case=False, na=False)
            ]

        if exam:
            df = df[(df["exam"].isna()) | (df["exam"].str.lower() == exam.lower())]

        if category:
            df = df[(df["category"].isna()) | (df["category"].str.lower() == category.lower())]

        if not df.empty and "year" in df:
            dedupe_subset = ["college_id", "course_id"]
            if exam:
                dedupe_subset.append("exam")
            if category:
                dedupe_subset.append("category")

            df = (
                df.sort_values("year", ascending=False, na_position="last")
                .drop_duplicates(
                    subset=dedupe_subset,
                    keep="first",
                )
            )

        if max_total_fees is not None:
            df = df[
                (df["total_fees"].isna()) |
                (df["total_fees"] <= float(max_total_fees))
            ]

        if min_package is not None:
            df = df[
                (df["average_package_lpa"].isna()) |
                (df["average_package_lpa"] >= float(min_package))
            ]

        if max_rank is not None:
            df = df[
                (df["closing_rank"].isna()) |
                (df["closing_rank"] >= int(max_rank))
            ]

        df = rank_recommendations(df, student_rank=max_rank)

        columns = [
            "college_id",
            "college_name",
            "course_name",
            "specialization",
            "city",
            "state",
            "ownership",
            "nirf_rank",
            "total_fees",
            "average_package_lpa",
            "median_package_lpa",
            "highest_package_lpa",
            "placement_percentage",
            "exam",
            "category",
            "closing_rank",
            "year",
            "scholarship_available",
            "website",
            "recommendation_score",
        ]
        return df[[column for column in columns if column in df]].head(limit).reset_index(drop=True)

    def recommend_as_records(self, **preferences: Any) -> list[dict[str, Any]]:
        frame = self.recommend(**preferences)
        records = frame.where(pd.notna(frame), None).to_dict(orient="records")
        return [_json_safe(record) for record in records]

    def metadata(self) -> dict[str, Any]:
        return {
            "analytics_backend": self.backend,
            "states": sorted(self.colleges["state"].dropna().unique().tolist()),
            "courses": sorted(self.courses["course_name"].dropna().unique().tolist()),
            "ownership_types": sorted(self.colleges["ownership"].dropna().unique().tolist()),
            "exams": sorted(self.cutoffs["exam"].dropna().unique().tolist()),
            "categories": sorted(self.cutoffs["category"].dropna().unique().tolist()),
            "college_count": int(self.colleges["college_id"].nunique()),
            "course_count": int(self.courses["course_id"].nunique()),
        }


def _json_safe(record: dict[str, Any]) -> dict[str, Any]:
    safe_record = {}
    for key, value in record.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            safe_record[key] = None
        else:
            safe_record[key] = value
    return safe_record
