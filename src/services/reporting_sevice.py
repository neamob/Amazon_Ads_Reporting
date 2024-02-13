from src.clients.amazon_ads_products_reporting_client import AmazonAdsProductsReportingClient


class ReportingService():
    
    def __init__(self,region:str,profile:str,report__start_date:str,report_end_date:str,schema_file:str) -> None:
       self.region=region
       self.profile=profile
       self.report__start_date=report__start_date
       self.report_end_date=report_end_date
       self.schema_file=schema_file
     
    
    
    
    def get_report(self):
        return AmazonAdsProductsReportingClient(region=self.region,profile=self.profile,report__start_date=self.report__start_date,report_end_date=self.report_end_date,schema_file=self.schema_file).get_report()