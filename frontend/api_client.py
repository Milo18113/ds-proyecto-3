import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class ApiClient:
    def __init__(self, token=None):
        self.base_url = API_BASE_URL
        self.token = token

    def _headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email, password):
        return requests.post(
            f"{self.base_url}/login",
            data={"username": email, "password": password},
            headers=self._headers(),
            timeout=10,
        )

    def me(self):
        return requests.get(
            f"{self.base_url}/me",
            headers=self._headers(),
            timeout=10,
        )

    # ── Incidents ─────────────────────────────────────────────────────────

    def get_incidents(self):
        return requests.get(
            f"{self.base_url}/incidents",
            headers=self._headers(),
            timeout=10,
        )

    def create_incident(self, payload):
        return requests.post(
            f"{self.base_url}/incidents",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )

    def get_incident_detail(self, incident_id):
        return requests.get(
            f"{self.base_url}/incidents/{incident_id}",
            headers=self._headers(),
            timeout=10,
        )

    def assign_incident(self, incident_id, payload):
        return requests.patch(
            f"{self.base_url}/incidents/{incident_id}/assign",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )

    def change_incident_status(self, incident_id, payload):
        return requests.patch(
            f"{self.base_url}/incidents/{incident_id}/status",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )

    # ── Tasks ─────────────────────────────────────────────────────────────

    def get_tasks(self):
        return requests.get(
            f"{self.base_url}/tasks",
            headers=self._headers(),
            timeout=10,
        )

    def create_task(self, payload):
        return requests.post(
            f"{self.base_url}/tasks",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )

    def update_task_status(self, task_id, payload):
        return requests.patch(
            f"{self.base_url}/tasks/{task_id}/status",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )

    # ── Notifications ─────────────────────────────────────────────────────

    def get_notifications(self):
        return requests.get(
            f"{self.base_url}/notifications",
            headers=self._headers(),
            timeout=10,
        )

    # ── Users ─────────────────────────────────────────────────────────────

    def get_users(self):
        return requests.get(
            f"{self.base_url}/users",
            headers=self._headers(),
            timeout=10,
        )
