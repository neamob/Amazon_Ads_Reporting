import requests
import json
from datetime import datetime, timedelta

# Constants

# Constants
CLIENT_ID = 'amzn1.application-oa2-client.1d802a1024654646a0f746779b03b56b'
CLIENT_SECRET = 'amzn1.oa2-cs.v1.9779ab7a2ce1028960aeec86f453b2f37ff91ddbf144de94ad40b9292f078599'
REFRESH_TOKEN = 'Atzr|IwEBIDr7HrR4jw3In2ov0uzPHnLJoxJO012YJJufO04yEfNzIXZYc7KgOTent9VrcBtX2urGTukX1-YSbr3fD-Bauc2CYP5V3h933UrttUl1AHkCITKonzt42GbHAS4vBG7dhnhiiF9Q58Nb5FtOiQsy8pDel5liRg9UfoFslqoIhqnp7OxeneEDBE6g0G4vvEr1-Veo_9vVq7RIW9_NUGhmP67tZR_UQB9xGXrK8wFN-KREd5euptuh-_scZoJE_TMix8eP83VmLOo3fJV0KcU3ruJAzuVYOSG3VyXnSV6Nm3iR43r3JlaUK0SE_eNTchCF7-erf2G-sC7Umsc0iZjn53xmDfhaSwV_Z3R-7_4zny6YmLqCt30uVe9ed2vobw6nZV3Ynscg6pzYn3lQdhVnJxQW31qNZe-TCXnrQCL0hO5TzoW6dUQ4YniwNw3NdBNAjNfEb0VD14YwnuJRxctDf2HfLMTZ4MnSN8sjLYrQO6ZW3kEy-T_RJgtswK7R0KDgKZsQ9OBK7kDiKHmFuyWY102o-628-zCzhgJjL9rusz6NgQ'
GRANT_TYPE = 'refresh_token'
REGION = 'NA'  # North American region
PROFILE_ID = '229917255141766'

def get_access_token():
    url = 'https://api.amazon.com/auth/o2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': GRANT_TYPE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['access_token']
    else:
        print("Failed to obtain access token.")
        return None
ACCESS_TOKEN = get_access_token()

# Function to request a Sponsored Products campaign report
def request_sp_campaign_report(access_token, profile_id, start_date, end_date):
    url = 'https://advertising-api.amazon.com/reporting/reports'
    headers = {
        'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
        'Amazon-Advertising-API-ClientId': CLIENT_ID,
        'Amazon-Advertising-API-Scope': profile_id,
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "name": "SP campaigns daily report",
        "startDate": start_date,
        "endDate": end_date,
        "configuration": {
            "adProduct": "SPONSORED_PRODUCTS",
            "groupBy": ["campaign"],
            "columns": ["campaignName","campaignId","impressions", "clicks", "cost", "date", "purchases14d", "sales14d"],
            "reportTypeId": "spCampaigns",
            "timeUnit": "DAILY",
            "format": "GZIP_JSON"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202:
        report_id = response.json().get('reportId')
        print(f"Report request submitted successfully. Report ID: {report_id}")
        return report_id
    else:
        print(f"Failed to request report: {response.text}")
        return None

# Example usage
if __name__ == '__main__':
    # Adjust these dates to your desired reporting period
    start_date = '2024-01-01'
    end_date = '2024-01-02'
    report_id = request_sp_campaign_report(ACCESS_TOKEN, PROFILE_ID, start_date, end_date)
    # You would then poll for the report status and download it once ready, as discussed previously.
