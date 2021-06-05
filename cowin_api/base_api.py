import requests
from fake_useragent import UserAgent


class BaseApi:

    def _call_api(self, url: str) -> dict:
        user_agent = UserAgent()
        headers = {'User-Agent': user_agent.random}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
