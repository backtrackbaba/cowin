from typing import Union

import requests
from fake_useragent import UserAgent
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class BaseApi:

    def _call_api(self, url) -> Union[HTTPError, dict]:
        user_agent = UserAgent()

        # parameters for retry
        retry_strategy = Retry(
            total=3,
            backoff_factor=1, # default is 0 and must be non zero
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        headers = {'User-Agent': user_agent.random}
        response = http.get(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # return an empty dictionary for consistency downstream
            print(f'[ERROR] {e}')
            return {}
        except e:
            print(f'[ERROR] {e}')
            return {}

        return response.json()
