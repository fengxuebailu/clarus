"""
Test ONLY the fixed parallel_simulation method
Clean test with fresh KataGo instance
"""

import asyncio
from app.agents.grandmaster import GrandmasterAgent
from app.core.katago_client import shutdown_katago_client


async def main():
    print("="*60)
    print("PARALLEL SIMULATION TEST (Sequential Execution)")
    print("="*60)

    agent = GrandmasterAgent(use_katago=True)
    board_state = "(;GM[1]FF[4]SZ[19])"  # Empty board

    print("\n[Test] Running parallel_simulation for Q16 vs D4...")
    print("[Test] (Note: Actually runs sequentially for stability)")

    try:
        vector_a, vector_b = await agent.parallel_simulation(
            board_state=board_state,
            move_a="Q16",
            move_b="D4",
            visits=500  # Low visits for speed
        )

        print("\n" + "="*60)
        print("RESULTS:")
        print("="*60)

        print(f"\nMove A (Q16):")
        print(f"  Winrate: {vector_a.winrate:.4f}")
        print(f"  Lead: {vector_a.lead:.2f}")
        print(f"  Visits: {vector_a.visits}")
        print(f"  Ownership: {len(vector_a.ownership)}x{len(vector_a.ownership[0])}")

        print(f"\nMove B (D4):")
        print(f"  Winrate: {vector_b.winrate:.4f}")
        print(f"  Lead: {vector_b.lead:.2f}")
        print(f"  Visits: {vector_b.visits}")
        print(f"  Ownership: {len(vector_b.ownership)}x{len(vector_b.ownership[0])}")

        print(f"\nDelta:")
        print(f"  Winrate diff: {abs(vector_a.winrate - vector_b.winrate):.4f}")
        print(f"  Lead diff: {abs(vector_a.lead - vector_b.lead):.2f}")

        # Check if real data
        is_mock_a = (vector_a.winrate == 0.68 and vector_a.lead == 12.5)
        is_mock_b = (vector_b.winrate == 0.68 and vector_b.lead == 12.5)

        print("\n" + "="*60)
        if is_mock_a or is_mock_b:
            print("STATUS: FAILED - Using mock data")
            print("="*60)
        else:
            print("STATUS: SUCCESS - Real KataGo data!")
            print("="*60)
            print("\nParallel simulation is working correctly!")

    except Exception as e:
        import traceback
        print("\n" + "="*60)
        print("STATUS: FAILED")
        print("="*60)
        print(f"Exception: {type(e).__name__}: {e}")
        print(f"Traceback:\n{traceback.format_exc()}")

    # Cleanup
    await shutdown_katago_client()
    print("\nKataGo client shut down.")


if __name__ == "__main__":
    asyncio.run(main())
