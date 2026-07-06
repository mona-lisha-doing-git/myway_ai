from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BigQueryConfig:
    project_id: str
    dataset: str
    location: str | None
    credentials_path: str | None
    max_bytes_billed: int | None
    row_limit: int | None
    colleges_table: str
    courses_table: str
    placements_table: str
    cutoffs_table: str

    @classmethod
    def from_env(cls) -> "BigQueryConfig":
        project_id = (
            os.getenv("BIGQUERY_PROJECT_ID")
            or os.getenv("GOOGLE_CLOUD_PROJECT")
            or os.getenv("GCLOUD_PROJECT")
        )
        dataset = os.getenv("BIGQUERY_DATASET")

        missing = []
        if not project_id:
            missing.append("BIGQUERY_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
        if not dataset:
            missing.append("BIGQUERY_DATASET")
        if missing:
            raise RuntimeError(
                "Missing required BigQuery configuration: "
                + ", ".join(missing)
                + ". Configure these environment variables before starting MyWay AI."
            )

        return cls(
            project_id=project_id,
            dataset=dataset,
            location=os.getenv("BIGQUERY_LOCATION"),
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            max_bytes_billed=_optional_int("BIGQUERY_MAX_BYTES_BILLED"),
            row_limit=_optional_int("BIGQUERY_TABLE_ROW_LIMIT"),
            colleges_table=os.getenv("BIGQUERY_COLLEGES_TABLE", "colleges"),
            courses_table=os.getenv("BIGQUERY_COURSES_TABLE", "courses"),
            placements_table=os.getenv("BIGQUERY_PLACEMENTS_TABLE", "placements"),
            cutoffs_table=os.getenv("BIGQUERY_CUTOFFS_TABLE", "cutoffs"),
        )


def _optional_int(name: str) -> int | None:
    value = os.getenv(name)
    if not value:
        return None
    try:
        parsed = int(value)
        if parsed <= 0:
            raise ValueError
        return parsed
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a positive integer.") from exc
