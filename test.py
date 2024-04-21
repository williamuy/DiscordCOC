import requests
import urllib.parse

class Barcher(object):
    def __init__(self, token):
        self.requests = requests
        self.token = token
        self.api_endpoint = "https://api.clashofclans.com/v1"
        self.timeout = 30  # Define the timeout attribute here

    def get(self, uri, params=None):
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + self.token
        }
        url = self.api_endpoint + uri
        try:
            response = self.requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()  # Raises an HTTPError if the response status is 4xx or 5xx
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": "HTTP error occurred", "status_code": response.status_code, "details": str(err)}
        except requests.exceptions.RequestException as err:
            return {"error": "Request exception occurred", "details": str(err)}

    def find_clan(self, tag):
        encoded_tag = urllib.parse.quote(tag)  # URL encode the clan tag
        return self.get('/clans/' + encoded_tag)
    
    

# Usage

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COC_API_KEY = os.getenv("COC_API_KEY")


barcher = Barcher(COC_API_KEY)
clan_info = barcher.find_clan('#2QRYUV9VP')
print(clan_info)
