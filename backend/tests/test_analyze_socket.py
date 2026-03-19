"""
Test analyze endpoint using socket
"""
import socket
import json
import time

def test_analyze():
    print("\n[Test] Testing /api/go/analyze endpoint...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(90)  # 90 second timeout for analysis
        sock.connect(('127.0.0.1', 8000))
        print("[Test] Connected to server")

        # Prepare request payload
        payload = {
            "board_state": "",
            "move_a": "Q16",
            "move_b": "D4",
            "player_color": "B"
        }

        json_body = json.dumps(payload)
        content_length = len(json_body)

        # HTTP POST request
        request = f"POST /api/go/analyze HTTP/1.1\r\n"
        request += f"Host: localhost:8000\r\n"
        request += f"Content-Type: application/json\r\n"
        request += f"Content-Length: {content_length}\r\n"
        request += f"\r\n"
        request += json_body

        print(f"[Test] Sending request ({content_length} bytes)...")
        print(f"[Test] Payload: {json_body}")
        sock.send(request.encode('utf-8'))

        print("[Test] Waiting for response...")
        start_time = time.time()

        # Read response
        response_data = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk

                # Check if we have complete response (look for end of JSON)
                if b"}" in response_data:
                    elapsed = time.time() - start_time
                    print(f"\n[Test] Response received ({len(response_data)} bytes, {elapsed:.1f}s)")

                    # Parse response
                    response_str = response_data.decode('utf-8', errors='ignore')
                    print(f"\n[Test] Response preview (first 1000 chars):")
                    print(response_str[:1000])
                    break

                # Progress indicator
                if int(time.time() - start_time) % 5 == 0:
                    print(f"[Test] Still waiting... ({int(time.time() - start_time)}s)")

            except socket.timeout:
                print(f"\n[Test] TIMEOUT after {time.time() - start_time:.1f}s")
                break

        sock.close()
    except Exception as e:
        print(f"[Test] ERROR: {e}")

if __name__ == "__main__":
    test_analyze()
