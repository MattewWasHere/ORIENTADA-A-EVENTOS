import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/") + "/"

    def get(self):
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json(), None

    def post(self, data):
        response = requests.post(self.base_url, json=data)
        response.raise_for_status()
        return response.json(), None

    def delete(self, identificador):
        url = f"{self.base_url}{identificador}/"
        response = requests.delete(url)
        response.raise_for_status()
        return {"ok": True}, None
