import asyncio
import datetime
from logging import Logger
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Json
from src.clients.amazon_ads_v2_reporting_client import AmazonAdsV2ReportingClient
from src.clients.bigquery_client import BigQueryClient
from src.services.reporting_sevice import ReportingService
from src.models.reports_models import AmazonReportBody

import datetime


def convert_date(date_str, date_format="%Y-%m-%d"):
    """
    Takes a date string, goes one day back, and returns the date in 'yyyymmdd' format.

    :param date_str: Date string in the format specified by date_format.
    :param date_format: Format of the input date string. Default is '%Y-%m-%d'.
    :return: String representing the date one day before date_str in 'yyyymmdd' format.
    """
    # Convert the string to a datetime object
    date_obj = datetime.datetime.strptime(date_str, date_format)
    
    # Subtract one day
    one_day_back = date_obj - datetime.timedelta(days=1)
    
    # Convert back to string in 'yyyymmdd' format
    one_day_back_str = one_day_back.strftime("%Y%m%d")
    
    return one_day_back_str



router = APIRouter()



@router.post("/get_ads_report")
async def get_ads_report(report_body:AmazonReportBody):
    

    amazon_client_report = ReportingService(report_body.region,report_body.profile,report_body.report__start_date,report_body.report_end_date,report_body.schema_file).get_report()
    bigquery_client = BigQueryClient(project_id=report_body.project_id).bq_table_from_df(df = amazon_client_report,project_id=report_body.project_id,dataset_id=report_body.dataset_id,table_id=report_body.table_id,writing_method=report_body.writing_method)

    return bigquery_client




@router.post("/get_ads_report/v2")
def get_ads_report(report_body:AmazonReportBody):
    
    start_date = datetime.datetime.strptime(report_body.report__start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(report_body.report_end_date, '%Y-%m-%d')

    current_date = start_date
    while current_date <= end_date:
        # Update the start date for each iteration
        report_body.report__start_date = current_date.strftime('%Y-%m-%d')
        date = convert_date(report_body.report__start_date)
        # Now call get_report() which uses the updated start date
        client = AmazonAdsV2ReportingClient(region=report_body.region,profile=report_body.profile,report__start_date=date,report_end_date=report_body.report_end_date,schema_file=report_body.schema_file)
        report = client.get_report()
        if report is not None and not report.empty:
            BigQueryClient(project_id=report_body.project_id).bq_table_from_df(df = report,project_id=report_body.project_id,dataset_id=report_body.dataset_id,table_id=report_body.table_id,writing_method=report_body.writing_method)

        current_date += datetime.timedelta(days=1)  # Move to the next date
        
    return {"message": "Reports fetched and uploaded successfully."}
    
   