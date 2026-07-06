from __future__ import annotations

import re
from dataclasses import dataclass

from google.cloud import bigquery

from utils.bigquery_config import BigQueryConfig


_PROJECT_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]{4,61}[A-Za-z0-9]$")
_DATASET_OR_TABLE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class QuerySpec:
    sql: str
    parameters: list[bigquery.ScalarQueryParameter]


@dataclass(frozen=True)
class BigQueryTable:
    project_id: str
    dataset: str
    table: str

    def sql_path(self) -> str:
        _validate_project_id(self.project_id)
        _validate_dataset_or_table(self.dataset, "dataset")
        _validate_dataset_or_table(self.table, "table")
        return f"`{self.project_id}.{self.dataset}.{self.table}`"


def dataset_table(config: BigQueryConfig, table_name: str) -> BigQueryTable:
    return BigQueryTable(
        project_id=config.project_id,
        dataset=config.dataset,
        table=table_name,
    )


def select_table_query(table: BigQueryTable, row_limit: int | None = None) -> QuerySpec:
    sql = f"SELECT * FROM {table.sql_path()}"
    parameters: list[bigquery.ScalarQueryParameter] = []
    if row_limit is not None:
        sql += " LIMIT @row_limit"
        parameters.append(bigquery.ScalarQueryParameter("row_limit", "INT64", row_limit))
    return QuerySpec(sql=sql, parameters=parameters)


def _validate_project_id(value: str) -> None:
    if not _PROJECT_ID_RE.match(value):
        raise ValueError(
            f"Invalid BigQuery project_id: {value!r}. Use a valid Google Cloud project ID."
        )


def _validate_dataset_or_table(value: str, label: str) -> None:
    if not _DATASET_OR_TABLE_RE.match(value):
        raise ValueError(
            f"Invalid BigQuery {label}: {value!r}. Use letters, numbers, and underscores only."
        )
