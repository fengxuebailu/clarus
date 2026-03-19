"""Test KataGo initialization"""
import asyncio
import sys
sys.path.append("D:\\ai\\Clarus\\backend")

from app.core.katago_client import get_katago_client

async def main():
    try:
        print("Testing KataGo client initialization...")
        client = await get_katago_client()
        print("SUCCESS! KataGo client initialized")
        print(f"Client running: {client.running}")
        print(f"Process PID: {client.process.pid if client.process else 'None'}")

        # Test a simple query
        print("\nTesting simple analysis query...")
        result = await client.analyze(
            moves=[],
            rules="chinese",
            komi=7.5,
            board_size=19,
            max_visits=10
        )
        print(f"Analysis result keys: {list(result.keys())}")
        print("Query test successful!")

        await client.stop()
        print("KataGo stopped cleanly")

    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
