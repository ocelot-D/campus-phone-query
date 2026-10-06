"""
HTTP 请求封装：统一处理 base_url、header、token、超时、日志
"""
import requests
import allure
from common.config import config


class ApiClient:
    def __init__(self, token=None):
        self.base_url = config.base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, params=None):
        return self._request('GET', path, params=params)

    def post(self, path, json=None, params=None):
        return self._request('POST', path, json=json, params=params)

    def _request(self, method, path, **kwargs):
        url = self._url(path)
        kwargs.setdefault('timeout', config.timeout)

        with allure.step(f"{method} {url}"):
            resp = self.session.request(method, url, **kwargs)
            allure.attach(
                f"Status: {resp.status_code}\nBody: {resp.text}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )

        # 解析 JSON 响应
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text}

        return resp.status_code, data
