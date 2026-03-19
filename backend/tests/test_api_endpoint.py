"""
Test the analyze API endpoint
"""
import requests
import json

def test_health():
    print("\n[Test] Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"[Test] Status: {response.status_code}")
        print(f"[Test] Response: {response.text}")
    except Exception as e:
        print(f"[Test] ERROR: {e}")

def test_analyze():
    print("\n[Test] Testing analyze endpoint...")
    payload = {
        "board_state": "",
        "move_a": "Q16",
        "move_b": "D4",
        "player_color": "B"
    }

    print(f"[Test] Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            "http://localhost:8000/api/go/analyze",
            json=payload,
            timeout=60
        )
        print(f"[Test] Status: {response.status_code}")
        print(f"[Test] Response: {response.text[:500]}")
    except Exception as e:
        print(f"[Test] ERROR: {e}")

if __name__ == "__main__":
    test_health()
    test_analyze()
