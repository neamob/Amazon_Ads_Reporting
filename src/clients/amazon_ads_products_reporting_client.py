from datetime import datetime, timedelta
import gzip
from io import BytesIO
import json
import time
import pandas as pd
import requests
from src.clients.amazon_reporting_helpers import load_report_schema
from src.clients.amazon_ads_reporting_client import AmazonAdsReportingClient



class AmazonAdsProductsReportingClient(AmazonAdsReportingClient):
    def __init__(self,profile,region,report__start_date,report_end_date,schema_file):
        super().__init__(profile,region)
        self.report_start_date = report__start_date
        self.report_end_date = report_end_date
        self.schema = schema_file
        if self.region=='EU':
            self.URL = "https://advertising-api-eu.amazon.com/reporting/reports"
        elif self.region=='NA':
             self.URL = "https://advertising-api.amazon.com/reporting/reports"
        elif self.region=='FA':
              self.URL = "https://advertising-api-fe.amazon.com/reporting/reports"
    
    def __create_report(self,) -> str:
        #create report_schema
        data = load_report_schema(self.schema)
        data["startDate"]=self.report_start_date
        data["endDate"]=self.report_end_date
        
        headers = self.generate_headers()
        try:
            response = requests.post(self.URL, headers=headers, data=json.dumps(data))
            
        
            return response.json()["reportId"]
        except Exception as e:
            self.logger.error(f"Failed to create report: {e}")
            print(response.text)
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
        check_url = f"{self.URL}/{report_id}"  # Adjust this URL to the correct endpoint
        headers = self.generate_headers()

        try:
            response = requests.get(check_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()["status"]
        except requests.RequestException as e:
            self.logger.error(f"Error checking report status: {e}")
            raise Exception(f"Error checking report status: {e}")

    def _get_report_download_url(self) -> str:
        check_url = f"{self.URL}/{self.report_id}"
        headers = self.generate_headers()

        try:
            response = requests.get(check_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()["url"]
        except requests.RequestException as e:
            self.logger.error(f"Error getting report URL: {e}")
            raise Exception(f"Error getting report URL: {e}")
    
    
    def get_report(self) -> pd.DataFrame:
        self.report_id = self.__create_report()
        #self.report_id = 'b053dcc1-9f6b-437a-89b5-07da211004e4'
        # Initiate report creation and get report ID
        #report_id = 'b43a6c12-f1e5-4b94-99c7-8c20501e2adc'  # Initiate report creation and get report ID
        # Initiate report creation and get report ID
        headers = self.generate_headers()
        
        end_time = datetime.now() + timedelta(minutes=20)
        while datetime.now() < end_time:
            status = self._check_report_status(self.report_id)  # Check report status
            if status == "COMPLETED":
                # Retrieve and return the report data as DataFrame
                REPORT_URL = self._get_report_download_url()
                return self._retrieve_report(REPORT_URL)
            elif status in ["FAILED", "CANCELLED"]:
                self.logger.error(f"Report generation failed or was cancelled. Status: {status}")
                return pd.DataFrame()  # Return an empty DataFrame or handle as appropriate
            self.logger.info(f"Report status: {status}. Waiting for 90 seconds...")
            
            
            time.sleep(90)  # Wait for 30 seconds before checking again

        raise TimeoutError("Report status check timed out after 15 minutes.")