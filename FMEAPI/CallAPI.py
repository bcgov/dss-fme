import os
import json
from FMEAPI.ApiException import APIException
from FMEAPI.api import APIConfig


class CallAPI:

    def __init__(self,  server, token):
        self.api_config = APIConfig()
        self.server = server
        self.token = token
        self.http_method = "GET"

    def execute_api(self, url, headers, body):
        pass

    def populate_url(self, method, url_params):
        root = self.api_config.api_url["api_root"] % self.server
        url = self.api_config.api_url[method]
        if url_params:
            url = url % tuple(url_params)
        if "token=" in url:
            url = url.replace("token=", "token=" + self.token)
        url = os.path.join(root, url)
        return url

    @staticmethod
    def api_call_return(response):
        result = {"response": response}
        if response.text:
            text = response.text.strip()
            if text and (text.startswith("{") or text.startswith("[")):
                result["text"] = json.loads(text)
        return result

    @staticmethod
    def api_call_success(response, return_codes):
        if return_codes:
            return response.ok and response.status_code in return_codes
        return response.ok

    def check_response(self, response, url, return_codes):
        if self.api_call_success(response, return_codes):
            return self.api_call_return(response)
        raise APIException(url, self.http_method, response)

    def call_api(self, method, url_params=None, return_codes=None, headers=None, body=None):
        url = self.populate_url(method, url_params)
        response = self.execute_api(url, headers, body)
        return self.check_response(response, url, return_codes)
