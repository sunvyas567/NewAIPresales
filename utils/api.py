import requests

API_BASE = "http://127.0.0.1:8001/api"

def api_get(path):
    return requests.get(f"{API_BASE}{path}").json()

def api_post(path, payload):
    return requests.post(f"{API_BASE}{path}", json=payload).json()
