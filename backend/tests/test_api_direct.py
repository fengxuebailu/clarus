"""
Direct API test - simulate frontend request
"""
import requests
import json

url = "http://localhost:8000/api/go/analyze"

data = {
    "board_state": "(;GM[1]FF[4]SZ[19])",
    "move_a": "Q16",
    "move_b": "D4",
    "player_color": "B"
}

print("Sending request to:", url)
print("Data:", json.dumps(data, indent=2))
print("\nWaiting for response...\n")

try:
    response = requests.post(url, json=data, timeout=120)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print("\n=== Analysis Result ===")
        print(f"Analysis ID: {result.get('analysis_id')}")
        print(f"Move A: {result.get('move_a')}")
        print(f"Move B: {result.get('move_b')}")

        if 'final_explanation' in result:
            exp = result['final_explanation']
            print(f"\nFinal Explanation:")
            print(f"  Text: {exp.get('explanation_text', '')[:200]}...")
            print(f"  Attempts: {exp.get('attempts_taken')}")
            print(f"  Validated: {exp.get('validation_passed')}")

        print("\nSUCCESS - API is working!")
    else:
        print(f"ERROR: {response.text}")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
