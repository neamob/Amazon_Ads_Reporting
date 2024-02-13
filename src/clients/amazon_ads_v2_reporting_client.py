from datetime import datetime, timedelta
import gzip
from io import BytesIO
import io
import json
import time
import pandas as pd
import requests
from src.clients.amazon_reporting_helpers import load_report_schema
from src.clients.amazon_ads_reporting_client import AmazonAdsReportingClient



class AmazonAdsV2ReportingClient(AmazonAdsReportingClient):
    def __init__(self,profile,region,report__start_date,report_end_date,schema_file):
        super().__init__(profile,region)
        self.report_start_date = report__start_date
        self.report_end_date = report_end_date
        self.schema = schema_file
        if self.region=='EU':
            self.URL = "https://advertising-api-eu.amazon.com/v2/hsa/campaigns/report"
            self.status_url = "https://advertising-api-eu.amazon.com/v2/reports"
        elif self.region=='NA':
             self.URL = "https://advertising-api.amazon.com/v2/hsa/campaigns/report"
             self.status_url = "https://advertising-api.amazon.com/v2/reports"
        elif self.region=='FA':
              self.URL = "https://advertising-api-fe.amazon.com/v2/hsa/campaigns/report"
              self.status_url = "https://advertising-api-fe.amazon.com/v2/reports"
        
    def __create_report(self) -> str:
        #create report_schema
        data = {
        "reportDate":self.report_start_date,
        "metrics": "impressions,campaignName,clicks,cost,attributedConversions14d,attributedSales14d",
        "creativeType": "all",
                }
        print(data)
        
       
        
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(self.URL, headers=headers, data=json.dumps(data))
            
        
            return response.json()["reportId"]
        except Exception as e:
            self.logger.error(f"Failed to create report: {e}")
            print(response)
            raise Exception("Failed to create report")
    
    def _retrieve_report(self, report_url:str) -> pd.DataFrame:
        
        

        try:
            # Fetch the report
            response = requests.get(report_url)
            response.raise_for_status()  # Ensure we got a successful response
            # Assuming the report is compressed in GZIP format
            compressed_file = BytesIO(response.content)
            with gzip.open(compressed_file, 'rt') as decompressed_file:
                # Assuming the report is in JSON format, convert it to a DataFrame
                # For JSON lines format
                data = json.load(decompressed_file)
                df = pd.json_normalize(data)
                
                # If the report is a regular JSON object (not lines), use:
                # data = json.load(decompressed_file)
                # df = pd.json_normalize(data)

                # If the report is in CSV format, directly read it into a DataFrame
                # df = pd.read_csv(decompressed_file)
                
            return df
        except requests.HTTPError as e:
            self.logger.error(f"Failed to download the report: {e}")
            raise Exception(f"Failed to download the report: {e}")
        except Exception as e:
            self.logger.error(f"Failed to download the report:{report_url}     {e}")
            raise Exception(f"Failed to download the report{report_url} {e}")
        
    def _check_report_status(self, report_id: str) -> str:
        check_url = f"{self.status_url}/{report_id}"  # Adjust this URL to the correct endpoint
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'

        try:
            response = requests.get(check_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()["status"]
        except requests.RequestException as e:
            self.logger.error(f"Error checking report status: {e}")
            raise Exception(f"Error checking report status: {e}")

    def _get_report_download_url(self) -> pd.DataFrame:
        check_url = f"{self.status_url}/{self.report_id}/download"
        headers = self.generate_headers()
        headers['Content-Type'] = 'application/json'
        response = requests.get(check_url, headers=headers,stream=True)
        compressed_file = io.BytesIO(response.content)  # extract .gz file
        decompressed_file = gzip.GzipFile(fileobj=compressed_file)  # unzip .gz file 
        pd_day =pd.read_json(decompressed_file)
        pd_day['date'] = self.report_start_date
        pd_day = pd_day[pd_day.cost != 0 ]
        #pd_day = pd_day.drop_duplicates()
        return pd_day

        # try:
        #     response = requests.get(check_url, headers=headers)
        #     response.raise_for_status()  # Raises an HTTPError if the response was an error
        #     return response.json()["url"]
        # except requests.RequestException as e:
        #     print(response.text)
        #     self.logger.error(f"Error getting report URL: {e}")
        #     raise Exception(f"Error getting report URL: {e}")
    
    
    def get_report(self) -> pd.DataFrame:
        self.report_id = self.__create_report()
        headers = self.generate_headers()
        
        end_time = datetime.now() + timedelta(minutes=20)
        while datetime.now() < end_time:
            status = self._check_report_status(self.report_id)  # Check report status
            if status == "SUCCESS":
                # Retrieve and return the report data as DataFrame
                REPORT_URL =  self._get_report_download_url()
                return REPORT_URL
            elif status in ["FAILED", "CANCELLED"]:
                self.logger.error(f"Report generation failed or was cancelled. Status: {status}")
                return pd.DataFrame()  # Return an empty DataFrame or handle as appropriate
            self.logger.info(f"Report {self.report_id} status: {status}. Waiting for 90 seconds...")
            
            
            time.sleep(90)  # Wait for 30 seconds before checking again

        raise TimeoutError("Report status check timed out after 15 minutes.")