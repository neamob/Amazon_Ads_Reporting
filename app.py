from logging import Logger
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Json
from src.clients.bigquery_client import BigQueryClient
from src.services.reporting_sevice import ReportingService
from src.models.reports_models import AmazonReportBody



router = APIRouter()



@router.post("/get_ads_report")
async def get_ads_report(report_body:AmazonReportBody):
    

    amazon_client_report = ReportingService(report_body.region,report_body.profile,report_body.report__start_date,report_body.report_end_date,report_body.schema_file).get_report()
    bigquery_client = BigQueryClient(project_id=report_body.project_id).bq_table_from_df(df = amazon_client_report,project_id=report_body.project_id,dataset_id=report_body.dataset_id,table_id=report_body.table_id,writing_method=report_body.writing_method)

    return bigquery_client
