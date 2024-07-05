import logging
import requests
from src.clients.secret_manager_client import SecretManagerClient


class AmazonAdsReportingClient:
    def __init__(self, profile,region):
        self.profile = profile
        self.region = region
        credentials = SecretManagerClient().get_secret_value()
       
            
        self.CLIENT_ID = credentials["CLIENT_ID"]
        self.CLIENT_SECRET = credentials["CLIENT_SECRET"]
        self.REFRESH_TOKEN = credentials["REGIONS"][region]["REFRESH_TOKEN"]
        self.PROFILE_ID = credentials["REGIONS"][region]["PROFILES"][profile]
        self.GRANT_TYPE = 'refresh_token'
        self.logger =logging.getLogger("Amazon Ads Reprting Logger")        
    def __get_access_token(self):
        url = 'https://api.amazon.com/auth/o2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': self.GRANT_TYPE,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'refresh_token': self.REFRESH_TOKEN
        }
        try:
            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
            return response_data['access_token']
        except Exception as e:
            print(f"Failed to obtain access token. {e}")
            return None
        
    def generate_headers(self):
        
        ACCESS_TOKEN = self.__get_access_token()
        headers = {
            'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
            'Amazon-Advertising-API-ClientId': f'{self.CLIENT_ID}',
            'Amazon-Advertising-API-Scope': f'{self.PROFILE_ID}',
            'Authorization': f'Bearer {ACCESS_TOKEN}',
        }
        return headers