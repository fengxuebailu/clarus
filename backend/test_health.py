"""
Quick health check for the backend server
"""
import requests
import os

os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
session = requests.Session()
session.trust_env = False

try:
    response = session.get("http://127.0.0.1:8000/health", timeout=5)
    print(f"Backend status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Backend NOT responding: {e}")
