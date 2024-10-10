import requests

class DefiDataCollector:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_defi_data(self):
        url = f"{self.base_url}/coins/markets"
        params = {'vs_currency': 'usd', 'category': 'decentralized_finance_defi', 'order': 'market_cap_desc', 'per_page': 100, 'page': 1}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}")