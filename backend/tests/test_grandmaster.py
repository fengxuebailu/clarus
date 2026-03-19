"""
Test script for Grandmaster Agent with real KataGo integration
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.grandmaster import GrandmasterAgent
from app.core.katago_client import get_katago_client


async def test_katago_direct():
    """Test KataGo client directly"""
    print("=" * 60)
    print("TEST 1: Direct KataGo Client Test")
    print("=" * 60)

    try:
        # Get KataGo client
        katago = await get_katago_client()
        print(f"[Test] KataGo client obtained - running: {katago.running}")

        # Test simple analysis: opening move at Q16
        print("\n[Test] Analyzing opening move: B Q16")
        result = await katago.analyze_position(
            moves=[("B", "Q16")],
            max_visits=1000  # Low visits for quick test
        )

        print(f"\n[Test] Analysis result:")
        print(f"  Winrate: {result.get('winrate', 'N/A')}")
        print(f"  Score Lead: {result.get('scoreLead', 'N/A')}")
        print(f"  Visits: {result.get('visits', 'N/A')}")
        print(f"  Ownership data points: {len(result.get('ownership', []))}")
        print(f"  Policy data points: {len(result.get('policy', []))}")

        return True

    except Exception as e:
        import traceback
        print(f"\n[Test] FAILED: {type(e).__name__}: {e}")
        print(f"[Test] Traceback:\n{traceback.format_exc()}")
        return False


async def test_grandmaster_single_move():
    """Test Grandmaster Agent single position analysis"""
    print("\n" + "=" * 60)
    print("TEST 2: Grandmaster Agent - Single Move Analysis")
    print("=" * 60)

    try:
        # Create Grandmaster agent with KataGo enabled
        agent = GrandmasterAgent(use_katago=True)
        print(f"[Test] Grandmaster agent created - use_katago: {agent.use_katago}")

        # Test empty board opening move
        print("\n[Test] Testing opening move Q16 on empty board")
        board_state = "(;GM[1]FF[4]SZ[19])"  # Empty board SGF

        result = await agent.analyze_position(
            board_state=board_state,
            move="Q16",
            visits=1000
        )

        print(f"\n[Test] Analysis result (GroundTruthVector):")
        print(f"  Winrate: {result.winrate}")
        print(f"  Lead: {result.lead}")
        print(f"  Visits: {result.visits}")
        print(f"  Ownership shape: {len(result.ownership)}x{len(result.ownership[0]) if result.ownership else 0}")
        print(f"  Saliency shape: {len(result.saliency)}x{len(result.saliency[0]) if result.saliency else 0}")
        print(f"  Move sequence: {result.move_sequence[:5]}...")

        # Verify it's not mock data
        is_mock = (result.winrate == 0.68 and result.lead == 12.5)
        if is_mock:
            print("\n[Test] WARNING: Looks like mock data!")
            return False
        else:
            print("\n[Test] SUCCESS: Real KataGo data!")
            return True

    except Exception as e:
        import traceback
        print(f"\n[Test] FAILED: {type(e).__name__}: {e}")
        print(f"[Test] Traceback:\n{traceback.format_exc()}")
        return False


async def test_grandmaster_parallel():
    """Test Grandmaster Agent parallel simulation"""
    print("\n" + "=" * 60)
    print("TEST 3: Grandmaster Agent - Parallel Simulation")
    print("=" * 60)

    try:
        agent = GrandmasterAgent(use_katago=True)

        # Test two opening moves
        board_state = "(;GM[1]FF[4]SZ[19])"  # Empty board
        move_a = "Q16"  # Corner approach
        move_b = "D4"   # Alternative corner

        print(f"\n[Test] Comparing moves: {move_a} vs {move_b}")

        vector_a, vector_b = await agent.parallel_simulation(
            board_state=board_state,
            move_a=move_a,
            move_b=move_b,
            visits=1000
        )

        print(f"\n[Test] Results:")
        print(f"\n  Move A ({move_a}):")
        print(f"    Winrate: {vector_a.winrate:.4f}")
        print(f"    Lead: {vector_a.lead:.2f}")

        print(f"\n  Move B ({move_b}):")
        print(f"    Winrate: {vector_b.winrate:.4f}")
        print(f"    Lead: {vector_b.lead:.2f}")

        print(f"\n  Delta:")
        print(f"    Winrate difference: {abs(vector_a.winrate - vector_b.winrate):.4f}")
        print(f"    Lead difference: {abs(vector_a.lead - vector_b.lead):.2f}")

        # Verify it's not mock data
        is_mock_a = (vector_a.winrate == 0.68 and vector_a.lead == 12.5)
        is_mock_b = (vector_b.winrate == 0.68 and vector_b.lead == 12.5)

        if is_mock_a or is_mock_b:
            print("\n[Test] WARNING: Looks like mock data!")
            return False
        else:
            print("\n[Test] SUCCESS: Real KataGo data!")
            return True

    except Exception as e:
        import traceback
        print(f"\n[Test] FAILED: {type(e).__name__}: {e}")
        print(f"[Test] Traceback:\n{traceback.format_exc()}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("GRANDMASTER AGENT + KATAGO INTEGRATION TEST")
    print("=" * 60)

    results = []

    # Test 1: Direct KataGo
    result1 = await test_katago_direct()
    results.append(("Direct KataGo Client", result1))

    # Test 2: Grandmaster single move
    result2 = await test_grandmaster_single_move()
    results.append(("Grandmaster Single Move", result2))

    # Test 3: Grandmaster parallel
    result3 = await test_grandmaster_parallel()
    results.append(("Grandmaster Parallel Simulation", result3))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\nALL TESTS PASSED!")
        print("KataGo integration is working correctly.")
    else:
        print("\nSOME TESTS FAILED")
        print("Check the error messages above for details.")

    print("=" * 60)

    # Cleanup
    from app.core.katago_client import shutdown_katago_client
    await shutdown_katago_client()
    print("\n[Test] KataGo client shut down")


if __name__ == "__main__":
    asyncio.run(main())
