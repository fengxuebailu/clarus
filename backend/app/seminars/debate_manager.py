"""
Debate Manager - Handles streaming debate state and resumption
Manages the real-time debate loop with human-in-the-loop continuation
"""

from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from ..schemas.go_analysis import (
    DeltaVector,
    ExplanationDraft,
    ReconstructionFeedback,
    ReconstructionIteration,
    PredictionTest
)
from ..agents.scribe import ScribeAgent
from ..agents.arbiter import ArbiterAgent
import uuid


class DebateState:
    """Persistent state for a debate session"""

    def __init__(self, debate_id: str, delta_vector: DeltaVector,
                 move_a: str, move_b: str, player_color: str,
                 board_state: str, punisher_sequence: List[str]):
        self.debate_id = debate_id
        self.delta_vector = delta_vector
        self.move_a = move_a
        self.move_b = move_b
        self.player_color = player_color
        self.board_state = board_state
        self.punisher_sequence = punisher_sequence

        # State tracking
        self.current_attempt = 0
        self.max_attempts = 3
        self.is_paused = False
        self.is_complete = False

        # History
        self.iterations: List[ReconstructionIteration] = []
        self.current_explanation: Optional[ExplanationDraft] = None
        self.current_feedback: Optional[ReconstructionFeedback] = None

        # Metadata
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class DebateManager:
    """
    Manages real-time debate sessions with streaming and resumption support
    """

    def __init__(self, scribe: Optional[ScribeAgent] = None,
                 arbiter: Optional[ArbiterAgent] = None):
        self.scribe = scribe or ScribeAgent()
        self.arbiter = arbiter or ArbiterAgent()

        # Active debate sessions
        self.debates: Dict[str, DebateState] = {}

    def create_debate(self, delta_vector: DeltaVector, move_a: str,
                      move_b: str, player_color: str, board_state: str,
                      punisher_sequence: List[str]) -> DebateState:
        """Create a new debate session"""
        debate_id = str(uuid.uuid4())

        state = DebateState(
            debate_id=debate_id,
            delta_vector=delta_vector,
            move_a=move_a,
            move_b=move_b,
            player_color=player_color,
            board_state=board_state,
            punisher_sequence=punisher_sequence
        )

        self.debates[debate_id] = state
        return state

    def get_debate(self, debate_id: str) -> Optional[DebateState]:
        """Retrieve an existing debate session"""
        return self.debates.get(debate_id)

    async def run_next_iteration(self, debate_id: str,
                                  on_message: Callable[[Dict[str, Any]], None]) -> bool:
        """
        Run the next iteration of the debate loop

        Args:
            debate_id: The debate session ID
            on_message: Callback function to send messages (e.g., via WebSocket)

        Returns:
            True if debate should continue, False if complete or paused
        """
        state = self.get_debate(debate_id)
        if not state:
            await on_message({
                "type": "error",
                "content": f"Debate {debate_id} not found"
            })
            return False

        # Check if already complete
        if state.is_complete:
            await on_message({
                "type": "system",
                "content": "Debate already complete",
                "status": "complete"
            })
            return False

        # Increment attempt counter
        state.current_attempt += 1
        state.updated_at = datetime.utcnow()

        attempt_num = state.current_attempt

        # Send attempt start message
        await on_message({
            "type": "system",
            "content": f"Starting Attempt {attempt_num}/{state.max_attempts}...",
            "attempt": attempt_num,
            "max_attempts": state.max_attempts
        })

        # Step 1: Scribe generates explanation
        await on_message({
            "type": "scribe_thinking",
            "content": "Scribe is drafting explanation..."
        })

        # Get previous feedback if exists
        previous_feedback = state.current_feedback.specific_feedback if state.current_feedback else None

        try:
            explanation = await self.scribe.generate_explanation(
                delta_vector=state.delta_vector,
                move_a=state.move_a,
                move_b=state.move_b,
                player_color=state.player_color,
                version=attempt_num,
                feedback=previous_feedback,
                punisher_sequence=state.punisher_sequence
            )
        except Exception as e:
            print(f"  [DebateManager] Scribe generate_explanation failed: {type(e).__name__}: {e}")
            await on_message({
                "type": "system",
                "content": f"Scribe encountered an error: {str(e)}. Retrying...",
                "status": "error"
            })
            # If scribe fails, we can't continue this iteration
            if state.current_attempt >= state.max_attempts:
                state.is_paused = True
                await on_message({
                    "type": "state",
                    "status": "paused",
                    "content": f"Scribe failed after {state.max_attempts} attempts. Click 'Continue Debate' to retry.",
                    "attempt": attempt_num
                })
                return False
            return True  # Try again

        state.current_explanation = explanation

        # Send Scribe's message
        await on_message({
            "type": "scribe",
            "content": explanation.general_maxim,
            "attempt": attempt_num,
            "full_explanation": {
                "situation_context": explanation.situation_context,
                "general_maxim": explanation.general_maxim,
                "detailed_analysis": explanation.detailed_analysis,
                "key_concepts": explanation.key_concepts
            }
        })

        # Step 2: Arbiter (Student) tests the explanation
        await on_message({
            "type": "student_thinking",
            "content": "Student is analyzing the maxim..."
        })

        try:
            feedback = await self.arbiter.test_prediction(
                explanation=explanation,
                board_state=state.board_state,
                move_a=state.move_a,
                move_b=state.move_b,
                player_color=state.player_color
            )
        except Exception as e:
            print(f"  [DebateManager] Student test_prediction failed: {type(e).__name__}: {e}")
            # Create a fallback feedback so the debate can continue
            feedback = ReconstructionFeedback(
                prediction_test=PredictionTest(
                    predicted_move="ERROR",
                    correct_move=state.move_a,
                    prediction_correct=False,
                    reasoning=f"Student encountered an error: {str(e)}"
                ),
                passed=False,
                specific_feedback=f"Student agent encountered a technical error: {str(e)}. The Scribe should try again with a clearer, more concise maxim.",
                error_score=1.0,
                missing_aspects=["technical_error"]
            )

        state.current_feedback = feedback

        # Send Student's response
        prediction_result = "correct" if feedback.passed else "incorrect"
        await on_message({
            "type": "student",
            "content": f"I predicted: {feedback.prediction_test.predicted_move}\n\n{feedback.prediction_test.reasoning}",
            "attempt": attempt_num,
            "prediction": {
                "predicted_move": feedback.prediction_test.predicted_move,
                "correct_move": feedback.prediction_test.correct_move,
                "result": prediction_result,
                "reasoning": feedback.prediction_test.reasoning
            }
        })

        # Step 3: System feedback
        if feedback.passed:
            # SUCCESS - Debate complete
            state.is_complete = True

            await on_message({
                "type": "system",
                "content": f"[OK] SUCCESS! Student correctly predicted {feedback.prediction_test.predicted_move}. The maxim is clear and actionable!",
                "status": "success",
                "attempt": attempt_num
            })

            return False  # Stop iteration

        else:
            # FAILURE - Provide feedback
            await on_message({
                "type": "system",
                "content": f"[X] FAILED! Student predicted {feedback.prediction_test.predicted_move}, but correct move was {feedback.prediction_test.correct_move}.\n\n{feedback.specific_feedback}",
                "status": "fail",
                "attempt": attempt_num,
                "feedback": feedback.specific_feedback
            })

            # Check if max attempts reached
            if state.current_attempt >= state.max_attempts:
                state.is_paused = True

                await on_message({
                    "type": "state",
                    "status": "paused",
                    "content": f"Maximum attempts ({state.max_attempts}) reached. Click 'Continue Debate' to try again.",
                    "attempt": attempt_num
                })

                return False  # Pause for human intervention

            else:
                # Continue to next attempt
                await on_message({
                    "type": "system",
                    "content": f"Continuing to Attempt {state.current_attempt + 1}...",
                    "status": "continuing"
                })

                return True  # Continue iteration

    def resume_debate(self, debate_id: str) -> bool:
        """
        Resume a paused debate

        Returns:
            True if successfully resumed, False otherwise
        """
        state = self.get_debate(debate_id)
        if not state:
            return False

        if not state.is_paused:
            return False

        # Reset pause state and allow continuation
        state.is_paused = False
        # Note: current_attempt is not reset - it continues from where it left off

        return True

    def cleanup_debate(self, debate_id: str):
        """Remove a debate session from memory"""
        if debate_id in self.debates:
            del self.debates[debate_id]
