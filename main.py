

import os
import uvicorn
from fastapi import FastAPI
from src.models.reports_models import AmazonReportBody
from src.clients.bigquery_client import BigQueryClient
from src.clients.amazon_ads_products_reporting_client import AmazonAdsProductsReportingClient

from src.clients.amazon_ads_reporting_client import AmazonAdsReportingClient
import logging
import app as appp

logging.basicConfig(level=logging.INFO)        
# amazon_client = AmazonAdsReportingClient(region="NA",profile="US")
# print(amazon_client.profile)
# print(amazon_client.PROFILE_ID)
# print(amazon_client.generate_headers())

app = FastAPI()

app.include_router(appp.router)
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# amazon_client_report = AmazonAdsProductsReportingClient(region="NA",profile="US",report__start_date="2024-01-01",report_end_date="2024-01-31",schema_file="display_report.json").get_report()
# bigquery_client = BigQueryClient(project_id="focus-sweep-394015").bq_table_from_df(project_id="focus-sweep-394015",df=amazon_client_report,dataset_id="bronze",table_id="amazon_ads_brand_campaigns",writing_method="append")

# test = AmazonReportBody(region="NA",profile="US",report__start_date="2024-01-01",report_end_date="2024-01-31",schema_file="display_report.json",project_id="focus-sweep-394015",dataset_id="bronze",table_id="amazon_ads_brand_campaigns",writing_method="append")


# amazon_client_report = AmazonAdsProductsReportingClient(region="NA",profile="US",report__start_date="2024-02-01",report_end_date="2024-02-12",schema_file="brand_report.json").get_report()
# bigquery_client = BigQueryClient(project_id="focus-sweep-394015").bq_table_from_df(project_id="focus-sweep-394015",df=amazon_client_report,dataset_id="bronze",table_id="amazon_ads_brand_campaigns",writing_method="append")

