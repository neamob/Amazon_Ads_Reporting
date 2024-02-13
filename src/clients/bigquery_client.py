from google.cloud import bigquery
import logging
from google.api_core.exceptions import InvalidArgument, NotFound, PermissionDenied
from typing import Any, Dict, List, Literal, Optional
import pandas as pd
from pandas_gbq import to_gbq


class BigQueryClient:
    def __init__(self, project_id: str) -> str:
        self.gcloud_logger = logging.getLogger("Google Cloud Looging")
        self.project_id = project_id
        self.df_query_result = pd.DataFrame()

    @staticmethod
    def bq_table_from_df(
        df: pd.DataFrame,
        dataset_id: str,
        table_id: str,
        project_id: str,
        writing_method: str,
    ) -> None:
        df['ingestion_timestamp'] = pd.Timestamp.now()
        df.columns = ["".join(e for e in col if e.isalnum()) for col in df.columns]
        try:
            to_gbq(
                df,
                f"{dataset_id}.{table_id}",
                project_id=project_id,
                if_exists=writing_method,
                chunksize=10000,
            )
            bq_logger = logging.getLogger("BigQuery Logger")
            bq_logger.info("data has been loaded succefully")

        except Exception as e:
            raise ("Something went wrong with uploading data to BQ!")