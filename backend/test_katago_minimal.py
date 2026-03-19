"""
Minimal KataGo test - simplest possible request
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
        stderr=asyncio.subprocess.DEVNULL  # Ignore stderr for now
    )

    print(f"[Test] PID: {process.pid}, waiting 20 seconds for init...")
    await asyncio.sleep(20)

    # Correct request with moves field
    request = {
        "id": "test",
        "moves": [["B", "Q16"]],  # Must include moves!
        "rules": "chinese",
        "komi": 7.5,
        "boardXSize": 19,
        "boardYSize": 19,
        "maxVisits": 100
    }

    json_str = json.dumps(request) + "\n"
    print(f"[Test] Sending: {json_str.strip()}")

    process.stdin.write(json_str.encode('utf-8'))
    await process.stdin.drain()

    print("[Test] Waiting for response...")

    try:
        line = await asyncio.wait_for(process.stdout.readline(), timeout=10)
        print(f"[Test] SUCCESS! Response: {line.decode()[:200]}")
    except asyncio.TimeoutError:
        print("[Test] TIMEOUT - no response")

    process.kill()
    await process.wait()

asyncio.run(test())
