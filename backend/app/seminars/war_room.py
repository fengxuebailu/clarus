"""
Seminar I: The War Room (Micro-Level Analysis)
This is the core dialectical engine that orchestrates all agents
to produce validated, high-quality explanations through the Reconstruction Game
"""

import uuid
from datetime import datetime
from typing import Optional
from ..agents.grandmaster import GrandmasterAgent
from ..agents.scribe import ScribeAgent
from ..agents.profiler import ProfilerAgent
from ..agents.arbiter import ArbiterAgent
from ..agents.delta_hunter import DeltaHunterAgent
from ..schemas.go_analysis import (
    MoveAnalysis,
    AnalysisResult,
    ExplanationDraft,
    ReconstructionFeedback,
    ReconstructionIteration,
    EstimatedVector  # NEW: for prediction mode compatibility
)
from ..core.config import settings
from ..utils.knowledge_store import KnowledgeStore


class WarRoom:
    """
    The War Room - Dialectical Analysis Engine
    Implements the Reconstruction Game loop for move-by-move analysis

    Workflow:
    1. Grandmaster generates V_A and V_B (parallel simulation)
    2. Delta Hunter extracts ΔV and key differences
    3. LOOP (max 3 retries):
       a. Scribe generates explanation T_n
       b. Profiler reconstructs V_est from T_n
       c. Arbiter judges: if error < threshold -> DONE, else -> feedback to Scribe
    4. Output: Validated AnalysisResult
    """

    def __init__(
        self,
        grandmaster: Optional[GrandmasterAgent] = None,
        scribe: Optional[ScribeAgent] = None,
        profiler: Optional[ProfilerAgent] = None,
        arbiter: Optional[ArbiterAgent] = None,
        delta_hunter: Optional[DeltaHunterAgent] = None
    ):
        """Initialize all agents"""
        self.grandmaster = grandmaster or GrandmasterAgent()
        self.scribe = scribe or ScribeAgent()
        self.profiler = profiler or ProfilerAgent()
        self.arbiter = arbiter or ArbiterAgent()
        self.delta_hunter = delta_hunter or DeltaHunterAgent()
        self.knowledge_store = KnowledgeStore()

        self.max_retries = settings.MAX_RECONSTRUCTION_RETRIES

    async def analyze_move(
        self,
        analysis_request: MoveAnalysis
    ) -> AnalysisResult:
        """
        Complete analysis workflow for a single move comparison

        This is the main entry point - implements the full Reconstruction Game

        Args:
            analysis_request: Contains board state, move A, move B

        Returns:
            AnalysisResult with validated explanation
        """

        # Step 1: Parallel Simulation - Get ground truth from Grandmaster
        print(f"[War Room] Starting parallel simulation for {analysis_request.move_a} vs {analysis_request.move_b}")

        vector_a, vector_b = await self.grandmaster.parallel_simulation(
            board_state=analysis_request.board_state,
            move_a=analysis_request.move_a,
            move_b=analysis_request.move_b
        )

        # Step 2: Delta Extraction - Identify key differences
        print("[War Room] Delta Hunter analyzing differences...")

        delta_vector = self.delta_hunter.analyze_delta(vector_a, vector_b)

        print(f"[War Room] Delta: Winrate={delta_vector.delta_winrate * 100:.2f}%, "
              f"Lead={delta_vector.delta_lead:.2f} pts")

        # Step 3: The Reconstruction Loop
        # Extract punisher sequence from vector_b's principal variation
        punisher_sequence = vector_b.move_sequence if vector_b.move_sequence else []

        final_explanation, reconstruction_attempts, final_feedback, iterations = \
            await self._reconstruction_loop(
                delta_vector,
                analysis_request.move_a,
                analysis_request.move_b,
                analysis_request.player_color,
                analysis_request.board_state,  # NEW: pass board_state for prediction test
                punisher_sequence
            )

        # Step 4: Build final result
        analysis_result = AnalysisResult(
            analysis_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            board_state=analysis_request.board_state,
            move_a=analysis_request.move_a,
            move_b=analysis_request.move_b,
            vector_a=vector_a,
            vector_b=vector_b,
            delta_vector=delta_vector,
            final_explanation=final_explanation,
            reconstruction_attempts=reconstruction_attempts,
            reconstruction_iterations=iterations,
            final_error=final_feedback.error_score,
            reconstruction_passed=final_feedback.passed
        )

        # Step 5: Save learned principle to knowledge store
        if final_explanation:
            self.knowledge_store.add_record(
                general_maxim=final_explanation.general_maxim,
                situation_context=final_explanation.situation_context,
                key_concepts=final_explanation.key_concepts,
                move_a=analysis_request.move_a,
                move_b=analysis_request.move_b,
                board_state=analysis_request.board_state,
                detailed_analysis=final_explanation.detailed_analysis,
                reconstruction_passed=final_feedback.passed,
            )

        print(f"[War Room] Analysis complete! "
              f"Attempts: {reconstruction_attempts}, "
              f"Passed: {final_feedback.passed}, "
              f"Error: {final_feedback.error_score:.4f}, "
              f"Knowledge store: {self.knowledge_store.count()} records")

        return analysis_result

    async def _reconstruction_loop(
        self,
        delta_vector,
        move_a: str,
        move_b: str,
        player_color: str,
        board_state: str,  # NEW: for prediction test
        punisher_sequence: list = None
    ) -> tuple:
        """
        The core Reconstruction Game loop - NEW PREDICTION-BASED MODE

        Loop:
        1. Scribe (Mentor) generates golden_rule + detailed_analysis
        2. Arbiter (Student) tests if golden_rule can predict Move A
        3. If failed: provide feedback and retry
        4. If passed or max retries: return result

        Args:
            board_state: SGF board position for prediction test
            punisher_sequence: Opponent's best response to Move B (from KataGo PV)

        Returns:
            (final_explanation, attempt_count, final_feedback, iterations)
        """

        explanation = None
        feedback = None
        attempt = 0
        iterations = []

        # Query knowledge store for related principles the student already learned
        learned_principles = self.knowledge_store.find_by_keywords(
            delta_vector.key_differences[:3], max_results=3
        )
        if learned_principles:
            print(f"[Prediction Loop] Found {len(learned_principles)} related principles in knowledge store")

        for attempt in range(1, self.max_retries + 1):
            print(f"\n[Prediction Loop] Attempt {attempt}/{self.max_retries}")

            # Scribe (Mentor): Generate golden_rule + detailed_analysis
            print(f"  [Scribe-Mentor] Generating golden rule T_{attempt}...")
            if punisher_sequence:
                print(f"  [Scribe-Mentor] Punisher sequence: {', '.join(punisher_sequence[:5])}")

            explanation = await self.scribe.generate_explanation(
                delta_vector=delta_vector,
                move_a=move_a,
                move_b=move_b,
                player_color=player_color,
                version=attempt,
                feedback=feedback.specific_feedback if feedback else None,
                punisher_sequence=punisher_sequence,
                board_state=board_state,
                learned_principles=learned_principles
            )

            print(f"  [Scribe-Mentor] Golden Rule: {explanation.golden_rule[:100]}...")
            print(f"  [Scribe-Mentor] Detailed Analysis: {len(explanation.detailed_analysis)} chars")
            print(f"  [Scribe-Mentor] Key concepts: {', '.join(explanation.key_concepts)}")

            # Arbiter (Student): Test if golden_rule can predict Move A
            print(f"  [Arbiter-Student] Testing prediction with golden rule...")

            feedback = await self.arbiter.test_prediction(
                explanation=explanation,
                board_state=board_state,
                move_a=move_a,
                move_b=move_b,  # NEW: for coordinate censoring
                player_color=player_color
            )

            print(f"  [Arbiter-Student] Predicted: {feedback.prediction_test.predicted_move}, "
                  f"Correct: {feedback.prediction_test.correct_move}, "
                  f"Passed: {feedback.passed}")

            # Create dummy EstimatedVector for compatibility with ReconstructionIteration
            # Use absolute value of delta as a proxy for confidence/quality
            estimated_vector = EstimatedVector(
                winrate_estimate=min(1.0, max(0.0, abs(delta_vector.delta_winrate))),
                lead_estimate=abs(delta_vector.delta_lead),
                key_feature_shifts={},
                confidence=1.0 if feedback.passed else 0.0,
                explanation_used=explanation.golden_rule
            )

            # Store this iteration
            iteration = ReconstructionIteration(
                attempt_number=attempt,
                draft=explanation,
                estimated_vector=estimated_vector,
                feedback=feedback,
                status='approved' if feedback.passed else 'rejected'
            )
            iterations.append(iteration)

            # Decision point
            if feedback.passed:
                print(f"\n[Prediction Loop] SUCCESS on attempt {attempt}!")
                break
            else:
                print(f"  [Arbiter-Student] Feedback: {feedback.specific_feedback[:150]}...")

                if attempt == self.max_retries:
                    print(f"\n[Prediction Loop] Max retries reached. Using best attempt.")

        return explanation, attempt, feedback, iterations

    async def batch_analyze(
        self,
        analysis_requests: list[MoveAnalysis],
        parallel: bool = False
    ) -> list[AnalysisResult]:
        """
        Analyze multiple positions

        Args:
            analysis_requests: List of move comparisons to analyze
            parallel: If True, run analyses in parallel (faster but more resource-intensive)

        Returns:
            List of AnalysisResults
        """

        if parallel:
            import asyncio
            results = await asyncio.gather(
                *[self.analyze_move(req) for req in analysis_requests]
            )
            return results
        else:
            results = []
            for req in analysis_requests:
                result = await self.analyze_move(req)
                results.append(result)
            return results
