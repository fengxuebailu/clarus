"""
Simple connection test
"""
import socket
import time

def test_socket():
    print("\n[Test] Testing socket connection to localhost:8000...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 8000))
        if result == 0:
            print("[Test] Port 8000 is OPEN and accepting connections")

            # Try sending HTTP request
            print("[Test] Sending HTTP GET / request...")
            request = b"GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
            sock.send(request)

            time.sleep(1)

            response = sock.recv(4096)
            print(f"[Test] Response received ({len(response)} bytes):")
            print(response.decode('utf-8', errors='ignore')[:500])
        else:
            print(f"[Test] Port 8000 is CLOSED or unreachable (error code: {result})")
        sock.close()
    except Exception as e:
        print(f"[Test] ERROR: {e}")

if __name__ == "__main__":
    test_socket()
