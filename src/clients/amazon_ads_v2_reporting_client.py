from datetime import datetime, timedelta
import gzip
from io import BytesIO
import json
import pandas as pd
import httpx
import asyncio
from src.clients.amazon_reporting_helpers import load_report_schema
from src.clients.amazon_ads_reporting_client import AmazonAdsReportingClient


class AmazonAdsV2ReportingClient(AmazonAdsReportingClient):
    def __init__(self, profile, region, report__start_date, report_end_date, schema_file):
        super().__init__(profile, region)
        self.report_start_date = report__start_date
        self.report_end_date = report_end_date
        self.schema = schema_file
        if self.region == 'EU':
            self.URL = "https://advertising-api-eu.amazon.com/v2/hsa/campaigns/report"
            self.status_url = "https://advertising-api-eu.amazon.com/v2/reports"
        elif self.region == 'NA':
            self.URL = "https://advertising-api.amazon.com/v2/hsa/campaigns/report"
            self.status_url = "https://advertising-api.amazon.com/v2/reports"
        elif self.region == 'FA':
            self.URL = "https://advertising-api-fe.amazon.com/v2/hsa/campaigns/report"
            self.status_url = "https://advertising-api-fe.amazon.com/v2/reports"

    async def __create_report(self) -> str:
        data = {
            "reportDate": self.report_start_date,
            "metrics": "impressions,campaignName,clicks,cost,attributedConversions14d,attributedSales14d",
            "creativeType": "all",
        }
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'
        async with httpx.AsyncClient() as client:
            response = await client.post(self.URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["reportId"]

    async def _retrieve_report(self, report_url: str) -> pd.DataFrame:
        async with httpx.AsyncClient() as client:
            response = await client.get(report_url)
            response.raise_for_status()
            compressed_file = BytesIO(response.content)
            with gzip.open(compressed_file, 'rt') as decompressed_file:
                data = json.load(decompressed_file)
                df = pd.json_normalize(data)
            return df

    async def _check_report_status(self, report_id: str) -> str:
        check_url = f"{self.status_url}/{report_id}"
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'
        async with httpx.AsyncClient() as client:
            response = await client.get(check_url, headers=headers)
            response.raise_for_status()
            return response.json()["status"]

    async def _get_report_download_url(self) -> pd.DataFrame:
        check_url = f"{self.status_url}/{self.report_id}/download"
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(check_url, headers=headers)
            response.raise_for_status()
            compressed_file = BytesIO(await response.aread())
            with gzip.GzipFile(fileobj=compressed_file) as decompressed_file:
                pd_day = pd.read_json(decompressed_file)
                pd_day['date'] = self.report_start_date
                pd_day = pd_day[pd_day.cost != 0]
            return pd_day

    async def get_report(self) -> pd.DataFrame:
        self.report_id = await self.__create_report()
        end_time = datetime.now() + timedelta(minutes=20)
        while datetime.now() < end_time:
            status = await self._check_report_status(self.report_id)
            if status == "SUCCESS":
                report_df = await self._get_report_download_url()
                return report_df
            elif status in ["FAILED", "CANCELLED"]:
                self.logger.error(f"Report generation failed or was cancelled. Status: {status}")
                return pd.DataFrame()
            self.logger.info(f"Report {self.report_id} status: {status}. Waiting for 90 seconds...")
            await asyncio.sleep(90)
        raise TimeoutError("Report status check timed out after 20 minutes.")
