import requests


API_BASE_URL = "http://localhost:8000"


class ApiClient:
    def __init__(self, token=None):
        self.base_url = API_BASE_URL
        self.token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email, password):
        return requests.post(
            f"{self.base_url}/login",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=10,
        )

    def me(self):
        return requests.get(
            f"{self.base_url}/me",
            headers=self._headers(),
            timeout=10,
        )

    def get_incidents(self):
        return requests.get(
            f"{self.base_url}/incidents",
            headers=self._headers(),
            timeout=10,
        )

    def get_tasks(self):
        return requests.get(
            f"{self.base_url}/tasks",
            headers=self._headers(),
            timeout=10,
        )

    def get_notifications(self):
        return requests.get(
            f"{self.base_url}/notifications",
            headers=self._headers(),
            timeout=10,
        )