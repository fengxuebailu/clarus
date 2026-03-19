"""
Agent A: The Grandmaster (Grandmaster Agent)
Backbone: KataGo Engine
Function: Outputs Ground Truth Vector including winrate, lead, territory map, and saliency
Capability: Run parallel simulations for different moves
"""

from typing import Optional, Tuple, List
import aiohttp
import asyncio
import numpy as np
from ..schemas.go_analysis import GroundTruthVector
from ..core.config import settings
from ..core.katago_client import get_katago_client
from ..utils.go_board import parse_board_state


class GrandmasterAgent:
    """
    The Grandmaster - KataGo Interface
    Provides the mathematical ground truth for Go positions
    """

    def __init__(
        self,
        timeout: int = 30,
        use_katago: bool = True
    ):
        self.timeout = timeout
        self.use_katago = use_katago  # Set to False for testing with mock data

    async def analyze_position(
        self,
        board_state: str,
        move: str,
        visits: int = 100  # Reduced for CPU version
    ) -> GroundTruthVector:
        """
        Analyze a single position after a specific move

        Args:
            board_state: SGF or board position string
            move: Move to analyze (e.g., "Q16")
            visits: Number of MCTS visits

        Returns:
            GroundTruthVector with complete analysis
        """
        if not self.use_katago:
            # Use mock data for testing
            print("[Grandmaster] Using mock data (use_katago=False)")
            return self._generate_mock_data()

        try:
            print(f"[Grandmaster] Analyzing position with KataGo: move={move}, visits={visits}")

            # Get KataGo client
            katago = await get_katago_client()
            print(f"[Grandmaster] KataGo client ready: {katago.running}")

            # Parse board state and create move sequence
            from ..utils.go_board import SGFParser

            if board_state.startswith("(;"):
                parser = SGFParser(board_state)
                moves = parser.get_moves()
                print(f"[Grandmaster] Parsed {len(moves)} moves from SGF")
            else:
                moves = []
                print("[Grandmaster] Empty board (no moves)")

            # Determine whose turn it is
            if len(moves) == 0:
                next_color = "B"
            else:
                last_color = moves[-1][0]
                next_color = "W" if last_color == "B" else "B"

            print(f"[Grandmaster] Next player: {next_color}")

            # Add the move to analyze
            analysis_moves = moves + [(next_color, move)]
            print(f"[Grandmaster] Sending {len(analysis_moves)} moves to KataGo")

            # Call KataGo
            result = await katago.analyze_position(
                moves=analysis_moves,
                max_visits=visits
            )

            print(f"[Grandmaster] KataGo analysis complete - winrate: {result.get('winrate', 'N/A')}")

            # Parse result into GroundTruthVector
            return self._parse_katago_response(result)

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"[Grandmaster] ERROR in KataGo analysis:")
            print(f"[Grandmaster]   Exception: {type(e).__name__}: {e}")
            print(f"[Grandmaster]   Traceback:\n{error_trace}")
            print(f"[Grandmaster] Falling back to mock data")
            return self._generate_mock_data()

    async def parallel_simulation(
        self,
        board_state: str,
        move_a: str,
        move_b: str,
        visits: int = 100  # Reduced for CPU version
    ) -> Tuple[GroundTruthVector, GroundTruthVector]:
        """
        Run simulations for two different moves
        This is the core capability for contrastive learning

        Note: Uses sequential execution instead of parallel due to KataGo
        client communication constraints (single stdin/stdout stream).
        With asyncio.Lock in place, sequential is more reliable.

        Args:
            board_state: Current board position
            move_a: AI's best move
            move_b: User's move or alternative

        Returns:
            Tuple of (V_A, V_B) - ground truth vectors for both moves
        """
        # Run both analyses sequentially (KataGo client uses single pipe)
        print(f"[Grandmaster] Analyzing move A: {move_a}")
        vector_a = await self.analyze_position(board_state, move_a, visits)

        print(f"[Grandmaster] Analyzing move B: {move_b}")
        vector_b = await self.analyze_position(board_state, move_b, visits)

        return vector_a, vector_b

    def _parse_katago_response(self, data: dict) -> GroundTruthVector:
        """Parse KataGo JSON response into GroundTruthVector"""
        # KataGo returns ownership as flat array, convert to 19x19 grid
        ownership_flat = data.get("ownership", [])
        if ownership_flat and len(ownership_flat) == 361:  # 19x19
            ownership = [ownership_flat[i*19:(i+1)*19] for i in range(19)]
        else:
            ownership = [[0.0] * 19 for _ in range(19)]

        # Extract policy map (also flat array)
        policy_flat = data.get("policy", [])
        if policy_flat and len(policy_flat) == 361:
            saliency = [policy_flat[i*19:(i+1)*19] for i in range(19)]
        else:
            saliency = [[0.0] * 19 for _ in range(19)]

        # Get principal variation
        pv = data.get("pv", [])

        return GroundTruthVector(
            winrate=data.get("winrate", 0.5),
            lead=data.get("scoreLead", 0.0),
            ownership=ownership,
            saliency=saliency,
            visits=data.get("visits", 100),
            move_sequence=pv
        )

    def _generate_mock_data(self) -> GroundTruthVector:
        """
        Generate mock data for development/testing
        Replace this with actual KataGo integration
        """
        return GroundTruthVector(
            winrate=0.68,
            lead=12.5,
            ownership=[[0.0] * 19 for _ in range(19)],
            saliency=[[0.0] * 19 for _ in range(19)],
            visits=100,
            move_sequence=["Q16", "D4", "Q4", "D16"]
        )

    async def test_counterfactual(
        self,
        board_state: str,
        stone_to_remove: str,
        visits: int = 100
    ) -> float:
        """
        Test counterfactual scenarios for the Seminar of Theory
        Example: "If we remove stone X, does winrate drop significantly?"

        Args:
            board_state: Current position
            stone_to_remove: Position to remove (e.g., "Q16")
            visits: MCTS visits

        Returns:
            Winrate change (delta)
        """
        # Analyze original position
        original = await self.analyze_position(board_state, "", visits)

        # Analyze position with stone removed
        # TODO: Implement board manipulation logic
        modified_board = self._remove_stone(board_state, stone_to_remove)
        modified = await self.analyze_position(modified_board, "", visits)

        return original.winrate - modified.winrate

    def _remove_stone(self, board_state: str, position: str) -> str:
        """
        Remove a stone from the board
        TODO: Implement actual SGF/board manipulation
        """
        # Placeholder - implement SGF parsing and manipulation
        return board_state
