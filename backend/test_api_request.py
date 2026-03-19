"""Test API request to debug 422 error"""
import requests
import json

url = "http://localhost:8000/api/go/analyze"

# Simulate frontend request
data = {
    "board_state": "(;GM[1]FF[4]SZ[19])",
    "move_a": "Q16",
    "move_b": "D4",
    "player_color": "B"
}

print("Sending request to:", url)
print("Data:", json.dumps(data, indent=2))
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print()
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    print(f"Response text: {response.text}")
