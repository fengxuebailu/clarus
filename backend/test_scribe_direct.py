"""
Test Scribe agent directly to debug Gemini API issue
"""
import asyncio
import sys
sys.path.insert(0, 'D:/ai/Clarus/backend')

from app.agents.scribe import ScribeAgent
from app.schemas.go_analysis import DeltaVector

async def test_scribe():
    print("Creating Scribe agent...")
    scribe = ScribeAgent()

    # Create a simple delta vector
    delta = DeltaVector(
        delta_winrate=0.002,
        delta_lead=0.02,
        key_differences=["Test difference"],
        delta_ownership=[[0.0] * 19 for _ in range(19)],
        magnitude=0.002
    )

    print("\nCalling generate_explanation...")
    try:
        result = await scribe.generate_explanation(
            delta_vector=delta,
            move_a="Q16",
            move_b="D4",
            player_color="B",
            version=1
        )

        print(f"\nSUCCESS!")
        print(f"Explanation: {result.text}")
        print(f"Concepts: {result.key_concepts}")

    except Exception as e:
        print(f"\nFAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_scribe())
