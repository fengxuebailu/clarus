import asyncio
import os

async def test():
    katago_path = "D:/ai/katago-v1.16.4-eigen-windows-x64/katago.exe"
    config_path = "D:/ai/katago-v1.16.4-eigen-windows-x64/analysis_config.cfg"
    model_path = "D:/ai/katago-v1.16.4-eigen-windows-x64/kata1-b40c256-s11840935168-d2898845681.bin.gz"

    cmd = [
        katago_path,
        "analysis",
        "-config", config_path,
        "-model", model_path
    ]

    print(f"Command: {' '.join(cmd)}")
    print(f"KataGo exists: {os.path.exists(katago_path)}")
    print(f"Config exists: {os.path.exists(config_path)}")
    print(f"Model exists: {os.path.exists(model_path)}")
    print()

    try:
        print("Creating subprocess...")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print(f"Process created with PID: {process.pid}")

        # Wait a bit
        await asyncio.sleep(3)

        if process.returncode is not None:
            print(f"Process terminated with code: {process.returncode}")
            stderr_output = await process.stderr.read()
            stdout_output = await process.stdout.read()
            print(f"STDERR: {stderr_output.decode('utf-8', errors='ignore')[:500]}")
            print(f"STDOUT: {stdout_output.decode('utf-8', errors='ignore')[:500]}")
        else:
            print("Process is still running!")
            process.terminate()

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
