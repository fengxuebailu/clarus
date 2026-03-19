"""
Test KataGo with sequential requests (not parallel)
"""

import asyncio
from app.agents.grandmaster import GrandmasterAgent
from app.core.katago_client import shutdown_katago_client


async def main():
    print("="*60)
    print("SEQUENTIAL REQUESTS TEST")
    print("="*60)

    agent = GrandmasterAgent(use_katago=True)
    board_state = "(;GM[1]FF[4]SZ[19])"

    # Request 1
    print("\n[Test] Request 1: Analyzing Q16...")
    try:
        result1 = await agent.analyze_position(board_state, "Q16", visits=500)
        print(f"[Test] Result 1: winrate={result1.winrate:.4f}, lead={result1.lead:.2f}")
        print(f"[Test] SUCCESS - Request 1 completed")
    except Exception as e:
        print(f"[Test] FAILED - Request 1: {type(e).__name__}: {e}")
        return

    # Wait a bit
    await asyncio.sleep(2)

    # Request 2
    print("\n[Test] Request 2: Analyzing D4...")
    try:
        result2 = await agent.analyze_position(board_state, "D4", visits=500)
        print(f"[Test] Result 2: winrate={result2.winrate:.4f}, lead={result2.lead:.2f}")
        print(f"[Test] SUCCESS - Request 2 completed")
    except Exception as e:
        print(f"[Test] FAILED - Request 2: {type(e).__name__}: {e}")
        return

    print("\n" + "="*60)
    print("SEQUENTIAL TEST: ALL PASSED")
    print("="*60)

    # Cleanup
    await shutdown_katago_client()


if __name__ == "__main__":
    asyncio.run(main())
