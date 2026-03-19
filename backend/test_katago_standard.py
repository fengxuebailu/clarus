"""
Standard KataGo Analysis request based on documentation
"""
import asyncio
import json

async def test():
    cmd = [
        "D:/ai/katago-v1.16.4-eigen-windows-x64/katago.exe",
        "analysis",
        "-config", "D:/ai/katago-v1.16.4-eigen-windows-x64/analysis_config.cfg",
        "-model", "D:/ai/katago-v1.16.4-eigen-windows-x64/kata1-b40c256-s11840935168-d2898845681.bin.gz"
    ]

    print("[Test] Starting KataGo...")
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )

    print(f"[Test] PID: {process.pid}, waiting 20 seconds...")
    await asyncio.sleep(20)

    # Standard request format from KataGo docs
    requests = [
        # Test 1: Empty moves with minimal visits
        {
            "id": "empty-board",
            "moves": [],
            "rules": "chinese",
            "komi": 7.5,
            "boardXSize": 19,
            "boardYSize": 19,
            "maxVisits": 1,  # Just 1 visit!
            "analyzeTurns": [0]
        },
        # Test 2: One move
        {
            "id": "one-move",
            "moves": [["B","Q16"]],
            "rules": "chinese",
            "komi": 7.5,
            "boardXSize": 19,
            "boardYSize": 19,
            "analyzeTurns": [1]
        }
    ]

    for req in requests:
        json_str = json.dumps(req) + "\n"
        print(f"\n[Test] Sending: {req['id']}")
        print(f"[Test] Request: {json_str.strip()}")

        process.stdin.write(json_str.encode('utf-8'))
        await process.stdin.drain()

        print(f"[Test] Waiting for response...")

        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout=30)
            response = json.loads(line.decode())
            print(f"[Test] SUCCESS!")
            print(f"[Test] Response ID: {response.get('id')}")
            if 'error' in response:
                print(f"[Test] ERROR: {response['error']}")
            elif 'rootInfo' in response:
                print(f"[Test] Winrate: {response['rootInfo'].get('winrate', 'N/A')}")
            print(f"[Test] Response keys: {list(response.keys())}")
        except asyncio.TimeoutError:
            print(f"[Test] TIMEOUT")
        except Exception as e:
            print(f"[Test] ERROR: {e}")

    process.kill()
    await process.wait()
    print("\n[Test] Done")

asyncio.run(test())
