"""Test suggest-moves API endpoint"""
import requests
import json
import os

# Disable proxy for localhost
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

url = "http://localhost:8000/api/go/suggest-moves"
data = {
    "board_state": "(;GM[1]FF[4]SZ[19])",
    "player_color": "B"
}

print("Testing suggest-moves API...")
print(f"Request: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data, timeout=90, proxies={'http': None, 'https': None})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result.get('suggestions', []))} suggestions:")
        for i, sug in enumerate(result.get('suggestions', [])[:3], 1):
            print(f"  {i}. {sug.get('move')} - winrate: {sug.get('winrate'):.3f}, visits: {sug.get('visits')}")
    else:
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
