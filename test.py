import requests
import json
import pandas as pd
url = 'https://advertising-api.amazon.com/reporting/reports'
# Constants
CLIENT_ID = 'amzn1.application-oa2-client.1d802a1024654646a0f746779b03b56b'
CLIENT_SECRET = 'amzn1.oa2-cs.v1.9779ab7a2ce1028960aeec86f453b2f37ff91ddbf144de94ad40b9292f078599'
REFRESH_TOKEN = 'IwEBIB9qgJJbAhpEx0w134kJJzukMY0bIGdM3DxlH1Lfmu7YK5AbczjVbkDMtusyuQYOScc0cSbsJElt_Rif7Na0j8q5PflHWKmfmRuqybd2rifOD9kpsBXowFtFLyrcladuEh4P9FwuQVnBK1xxB4UBsXzEB1qkb6i5rMF3uljrlcUMaXah5TAXOW5Co62bFO12oW3A_YbJVbpJz0WYnH9MrNw2FndjsMXSSCaYAZCLtEeZATM9ubCFuNF1eOruINqChFZDkFAyD7yl_teadGMDQYWdlcQSadCT9QKelETf8W-HZz28BX75nFVTIxFE0qH8XHcmQQNFrg4HEhiLbvOP3G6Dm71r2_lowBD1W2hiu1MCZlNcdyzOUmGSJ2xpWOvMO98fPAag5gts3cy9NGWEwRZoIeQH_J_Ou1xqRxCc3Qu81VYsCPh-LanZ7sWmirlRwv-EJGIeK10uTGPfHeOXlBa_vjOtUS8_t6i2gaXjz0fcf6gk3HfFD4FqeJ7j2_LfUSObxsd2B8MvdBxCuveberjMco535lCpTuoOtiy7q_r-YA'
GRANT_TYPE = 'refresh_token'
REGION = 'NA'  # North American region
PROFILE_ID = '229917255141766'


# def get_access_token():
#     url = 'https://api.amazon.com/auth/o2/token'
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     data = {
#         'grant_type': GRANT_TYPE,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'refresh_token': REFRESH_TOKEN
#     }
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code == 200:
#         response_data = response.json()
#         return response_data['access_token']
#     else:
#         print("Failed to obtain access token.")
#         return None
    
# ACCESS_TOKEN = get_access_token()
# print(ACCESS_TOKEN)
# headers = {
#     'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
#     'Amazon-Advertising-API-ClientId': f'{CLIENT_ID}',
#     'Amazon-Advertising-API-Scope': f'{PROFILE_ID}',
#     'Authorization': f'Bearer {ACCESS_TOKEN}',
# }

# data = {
#     "name": "neamob-test",
#     "startDate": "2024-01-01",
#     "endDate": "2024-01-04",
#     "configuration": {
#         "adProduct": "SPONSORED_PRODUCTS",
#         "groupBy": ["campaign"],
#         "columns": ["impressions", "clicks", "cost", "campaignId","purchases14d", "sales14d"],
#         "reportTypeId": "spCampaigns",
#         "timeUnit": "DAILY",
#         "format": "GZIP_JSON"
#     }
# }

# response = requests.post(url, headers=headers, data=json.dumps(data))

# print(response.text)



import requests

url = 'https://advertising-api.amazon.com/reporting/reports/b5345b09-1f08-4294-8172-535c4a322430'

headers = {
    'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
    'Amazon-Advertising-API-ClientId': f'{CLIENT_ID}',
    'Amazon-Advertising-API-Scope': f'{PROFILE_ID}',
    'Authorization': f'Bearer Atza|IwEBIB9qgJJbAhpEx0w134kJJzukMY0bIGdM3DxlH1Lfmu7YK5AbczjVbkDMtusyuQYOScc0cSbsJElt_Rif7Na0j8q5PflHWKmfmRuqybd2rifOD9kpsBXowFtFLyrcladuEh4P9FwuQVnBK1xxB4UBsXzEB1qkb6i5rMF3uljrlcUMaXah5TAXOW5Co62bFO12oW3A_YbJVbpJz0WYnH9MrNw2FndjsMXSSCaYAZCLtEeZATM9ubCFuNF1eOruINqChFZDkFAyD7yl_teadGMDQYWdlcQSadCT9QKelETf8W-HZz28BX75nFVTIxFE0qH8XHcmQQNFrg4HEhiLbvOP3G6Dm71r2_lowBD1W2hiu1MCZlNcdyzOUmGSJ2xpWOvMO98fPAag5gts3cy9NGWEwRZoIeQH_J_Ou1xqRxCc3Qu81VYsCPh-LanZ7sWmirlRwv-EJGIeK10uTGPfHeOXlBa_vjOtUS8_t6i2gaXjz0fcf6gk3HfFD4FqeJ7j2_LfUSObxsd2B8MvdBxCuveberjMco535lCpTuoOtiy7q_r-YA',
}
response = requests.get(url, headers=headers)
response_json = response.json()  # Parse the JSON response
print(response_json)
status = response_json['status']  # Extract the status
print(status)



report_url = response_json['url']

# Make a GET request to download the report
response = requests.get(report_url)
response.raise_for_status() 

import csv
from io import StringIO

# Assuming the report is in CSV format


import gzip
from io import BytesIO

# Decompress GZIP content
compressed_file = BytesIO(response.content)
decompressed_file = gzip.open(compressed_file, 'rt')  # 'rt' for read text mode
with gzip.open(compressed_file, 'rt') as decompressed_file:

    # Load the JSON data (assuming the entire file is a single JSON object)
    data = json.load(decompressed_file)  # Use json.load() for single JSON object

    # If the JSON data is a list of objects, you don't need to wrap it with []
    # If it's a single JSON object, make it a list: [data]

    # Flatten the JSON data and convert to a DataFrame
    df = pd.json_normalize(data)  # For a list of objects
    # df = pd.json_normalize([data])  # Use this line instead if `data` is a single object

# Now df holds your data as a DataFrame
print(df.info())
print(df.head())

# Now, you can read the content as usual, e.g., if it's CSV
# csv_reader = csv.reader(decompressed_file)

# for row in csv_reader:
#     print(row)

# # Don't forget to close the decompressed file if you're done with it
# decompressed_file.close()
