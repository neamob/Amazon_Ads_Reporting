

import os
import uvicorn
from fastapi import FastAPI
from src.clients.amazon_ads_v2_reporting_client import AmazonAdsV2ReportingClient
from src.models.reports_models import AmazonReportBody
from src.clients.bigquery_client import BigQueryClient
from src.clients.amazon_ads_products_reporting_client import AmazonAdsProductsReportingClient

import logging
import app as appp

logging.basicConfig(level=logging.INFO)        

app = FastAPI()

app.include_router(appp.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


