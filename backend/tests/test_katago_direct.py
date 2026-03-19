"""
Direct test of KataGo Analysis Engine communication
"""
import asyncio
import json
import sys

async def test_katago():
    """Test KataGo communication directly"""

    cmd = [
        "D:/ai/katago-v1.16.4-eigen-windows-x64/katago.exe",
        "analysis",
        "-config", "D:/ai/katago-v1.16.4-eigen-windows-x64/analysis_config.cfg",
        "-model", "D:/ai/katago-v1.16.4-eigen-windows-x64/kata1-b40c256-s11840935168-d2898845681.bin.gz"
    ]

    print(f"[Test] Starting KataGo process...")
    print(f"[Test] Command: {' '.join(cmd)}")

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    print(f"[Test] Process started with PID: {process.pid}")
    print(f"[Test] Waiting for initialization...")

    # Read some stderr to see initialization
    async def read_stderr():
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            text = line.decode('utf-8', errors='ignore').strip()
            if text:
                print(f"[stderr] {text}")

    # Start stderr reader in background
    stderr_task = asyncio.create_task(read_stderr())

    # Wait for model to load
    print(f"[Test] Waiting 10 seconds for model to load...")
    await asyncio.sleep(10)

    # Prepare simple analysis request
    request = {
        "id": "test-1",
        "moves": [["B", "Q16"], ["W", "D4"]],  # With moves
        "rules": "chinese",
        "komi": 7.5,
        "boardXSize": 19,
        "boardYSize": 19,
        "maxVisits": 1,  # Minimal visits for fastest response
        "includeOwnership": False,
        "includePolicy": False
    }

    request_json = json.dumps(request) + "\n"
    print(f"\n[Test] Sending request:")
    print(f"[Test] {request_json.strip()}")

    process.stdin.write(request_json.encode())
    await process.stdin.drain()

    print(f"[Test] Request sent, waiting for response (30s timeout)...")

    try:
        # Try reading with periodic status updates
        for i in range(30):
            try:
                response_line = await asyncio.wait_for(
                    process.stdout.readline(),
                    timeout=1.0
                )

                if response_line:
                    print(f"\n[Test] SUCCESS! Received response:")
                    response = json.loads(response_line.decode())
                    print(json.dumps(response, indent=2)[:500])  # First 500 chars
                    break

            except asyncio.TimeoutError:
                if i % 5 == 0:
                    print(f"[Test] Still waiting... ({i}s elapsed)")
                continue
        else:
            print(f"\n[Test] ERROR: Timeout after 30s")
            print(f"[Test] Process still alive: {process.returncode is None}")

    except Exception as e:
        print(f"\n[Test] ERROR: {e}")

    # Cleanup
    stderr_task.cancel()
    process.kill()
    await process.wait()
    print(f"\n[Test] Process terminated")

if __name__ == "__main__":
    asyncio.run(test_katago())
