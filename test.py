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
barcher = Barcher('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjU1ODUzNjM1LTA1ZTAtNDNiZS1iZjE4LWU3YjgxYjUxZDUzYSIsImlhdCI6MTcxMzM3OTE0Niwic3ViIjoiZGV2ZWxvcGVyLzY5NGRhZDY2LTI1MTktMWRjMi0zNmU3LTRlMmZhYWY5OTRiNSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjY3LjE2OC40NS4yMzMiLCIyMDUuMTc1LjEwNi43NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.CeKtjpI_LNsSB6utOdtTYrSpuDoDyCUGN7W0nWU3l8u0FO8YCP_eJdk5VH2dGadoCSgEzu7d-iyy2tNV-X1YCQ')
clan_info = barcher.find_clan('#2QRYUV9VP')
print(clan_info)
