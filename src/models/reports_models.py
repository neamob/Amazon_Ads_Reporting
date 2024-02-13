from pydantic import BaseModel


class AmazonReportBody(BaseModel):
    region:str
    profile:str
    report__start_date:str
    report_end_date:str
    schema_file:str
    project_id:str
    dataset_id:str
    table_id:str
    writing_method:str
    
  