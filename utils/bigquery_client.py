from __future__ import annotations

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

from utils.bigquery_config import BigQueryConfig
from utils.bigquery_queries import QuerySpec


class BigQueryDataClient:
    def __init__(self, config: BigQueryConfig | None = None):
        self.config = config or BigQueryConfig.from_env()
        self.client = self._build_client()

    def _build_client(self) -> bigquery.Client:
        credentials = None
        if self.config.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                self.config.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

        return bigquery.Client(
            project=self.config.project_id,
            credentials=credentials,
            location=self.config.location,
        )

    def fetch_dataframe(self, query: QuerySpec) -> pd.DataFrame:
        job_config = bigquery.QueryJobConfig(
            query_parameters=query.parameters,
            use_legacy_sql=False,
        )
        if self.config.max_bytes_billed is not None:
            job_config.maximum_bytes_billed = self.config.max_bytes_billed

        query_job = self.client.query(
            query.sql,
            job_config=job_config,
            location=self.config.location,
        )
        return query_job.result().to_dataframe(create_bqstorage_client=False)
