from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from utils.bigquery_client import BigQueryDataClient
from utils.bigquery_config import BigQueryConfig
from utils.bigquery_queries import dataset_table, select_table_query


@dataclass(frozen=True)
class DatasetBundle:
    colleges: pd.DataFrame
    courses: pd.DataFrame
    placements: pd.DataFrame
    cutoffs: pd.DataFrame
    backend: str


def _normalize_columns(frame: Any) -> Any:
    frame.columns = (
        frame.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return frame


def load_datasets(config: BigQueryConfig | None = None) -> DatasetBundle:
    active_config = config or BigQueryConfig.from_env()
    client = BigQueryDataClient(active_config)

    colleges = _fetch_table(client, active_config, active_config.colleges_table)
    courses = _fetch_table(client, active_config, active_config.courses_table)
    placements = _fetch_table(client, active_config, active_config.placements_table)
    cutoffs = _fetch_table(client, active_config, active_config.cutoffs_table)

    return DatasetBundle(
        colleges=colleges,
        courses=courses,
        placements=placements,
        cutoffs=cutoffs,
        backend="bigquery",
    )


def _fetch_table(
    client: BigQueryDataClient,
    config: BigQueryConfig,
    table_name: str,
) -> pd.DataFrame:
    table = dataset_table(config, table_name)
    query = select_table_query(table, row_limit=config.row_limit)
    return _normalize_columns(client.fetch_dataframe(query))


def to_pandas(frame: Any) -> pd.DataFrame:
    if hasattr(frame, "to_pandas"):
        return frame.to_pandas()
    return frame.copy()
