import time
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
        df = df.astype(str)
        df.columns = ["".join(e for e in col if e.isalnum()) for col in df.columns]
        bq_logger = logging.getLogger("BigQuery Logger")
        max_retries = 3
        sleep_time = 20 
        for attempt in range(max_retries):
            try:
                to_gbq(
                    df,
                    f"{dataset_id}.{table_id}",
                    project_id=project_id,
                    if_exists=writing_method,
                    chunksize=10000,
                )
                bq_logger.info("Data has been loaded successfully")
                break  # Exit the loop on success
            except Exception as e:
                bq_logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(sleep_time)  # Wait before the next attempt
                else:
                    bq_logger.error("All attempts to upload data to BQ failed!")
                    raise Exception("Something went wrong with uploading data to BQ!") from e