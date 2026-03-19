from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum


class GroundTruthVector(BaseModel):
    """
    Ground Truth Vector from KataGo - represents the mathematical truth
    $V_{true}$ in the design document
    """
    winrate: float = Field(..., ge=0.0, le=1.0, description="Winrate (0.0 to 1.0)")
    lead: float = Field(..., description="Score lead in points")
    ownership: List[List[float]] = Field(..., description="19x19 territory ownership map (-1 to 1)")
    saliency: Optional[List[List[float]]] = Field(None, description="Saliency map highlighting important regions")
    visits: int = Field(..., description="Number of MCTS visits")
    move_sequence: List[str] = Field(default_factory=list, description="Principal variation (PV)")

    class Config:
        json_schema_extra = {
            "example": {
                "winrate": 0.68,
                "lead": 12.5,
                "ownership": [[0.0] * 19 for _ in range(19)],
                "saliency": [[0.0] * 19 for _ in range(19)],
                "visits": 10000,
                "move_sequence": ["Q16", "D4", "Q4"]
            }
        }


class EstimatedVector(BaseModel):
    """
    Estimated Vector from Profiler Agent
    $V_{est}$ - the Profiler's reconstruction from explanation text
    """
    winrate_estimate: float = Field(..., ge=0.0, le=1.0)
    lead_estimate: float
    key_feature_shifts: Dict[str, float] = Field(
        default_factory=dict,
        description="Identified feature changes (e.g., 'center_influence': -0.2)"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Profiler's confidence in reconstruction")
    explanation_used: str = Field(default="", description="The explanation text that was reconstructed from")


class DeltaVector(BaseModel):
    """
    Delta Vector - difference between two moves
    $\Delta V = V_A - V_B$
    """
    delta_winrate: float
    delta_lead: float
    delta_ownership: List[List[float]]
    key_differences: List[str] = Field(
        default_factory=list,
        description="Natural language summary of key differences"
    )
    magnitude: float = Field(..., description="Overall magnitude of difference")


class MoveAnalysis(BaseModel):
    """Input for analyzing a specific move"""
    board_state: str = Field(..., description="SGF or board position string")
    move_a: str = Field(..., description="Move A (AI best move, e.g., 'Q16')")
    move_b: str = Field(..., description="Move B (User/Alternative move, e.g., 'D4')")
    player_color: str = Field(..., description="'B' for Black, 'W' for White")


class ExplanationDraft(BaseModel):
    """
    Draft explanation from Scribe Agent (The Mentor)
    NEW: Separated into Context (specific) vs. Concept (abstract)
    """
    situation_context: str = Field(
        ...,
        description="Specific board pattern description (e.g., 'Opponent has a low stone on third line with developing moyo above'). NO coordinates."
    )
    general_maxim: str = Field(
        ...,
        description="Abstract, generalizable Go principle (e.g., 'Press down on low stones to build influence, don't try to kill'). Must apply to ANY similar situation."
    )
    detailed_analysis: str = Field(..., description="Full tactical breakdown with specific coordinates (for logging/debugging)")
    version: int = Field(default=1, description="Version number (T_1, T_2, etc.)")
    key_concepts: List[str] = Field(
        default_factory=list,
        description="Go concepts used (e.g., 'Thickness', 'Aji', 'Shape')"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @property
    def text(self) -> str:
        """Legacy compatibility - returns general_maxim"""
        return self.general_maxim

    @property
    def golden_rule(self) -> str:
        """Legacy compatibility - returns general_maxim"""
        return self.general_maxim


class PredictionTest(BaseModel):
    """Result of Arbiter's prediction test"""
    predicted_move: str = Field(..., description="Move predicted by Arbiter based on golden_rule")
    correct_move: str = Field(..., description="The actual correct move (Move A)")
    prediction_correct: bool = Field(..., description="Whether prediction matched Move A")
    reasoning: str = Field(..., description="Arbiter's explanation of why it chose this move")

class ReconstructionFeedback(BaseModel):
    """Feedback from Arbiter (The Student) to Scribe (The Mentor)"""
    prediction_test: PredictionTest = Field(..., description="Result of prediction-based verification")
    passed: bool = Field(..., description="Whether the golden_rule successfully guided to Move A")
    specific_feedback: str = Field(
        ...,
        description="Why the rule worked or failed (e.g., 'Your rule said defend corner, so I played R3, but correct was Q4')"
    )
    error_score: float = Field(default=0.0, description="Legacy field - always 0 in prediction mode")
    missing_aspects: List[str] = Field(default_factory=list)


class ReconstructionIteration(BaseModel):
    """Single iteration of the reconstruction loop"""
    attempt_number: int = Field(..., description="Iteration number (1, 2, 3)")
    draft: ExplanationDraft = Field(..., description="Explanation from Scribe")
    estimated_vector: EstimatedVector = Field(..., description="Profiler's reconstruction")
    feedback: ReconstructionFeedback = Field(..., description="Arbiter's judgment")
    status: str = Field(..., description="'approved' or 'rejected'")


class AnalysisResult(BaseModel):
    """
    Final analysis result - saved to user's personal library
    This is the complete output from the War Room
    """
    analysis_id: str = Field(..., description="Unique identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Input data
    board_state: str
    move_a: str
    move_b: str

    # Ground truth data
    vector_a: GroundTruthVector
    vector_b: GroundTruthVector
    delta_vector: DeltaVector

    # Explanation
    final_explanation: ExplanationDraft
    reconstruction_attempts: int = Field(..., description="Number of Scribe-Profiler iterations")
    reconstruction_iterations: List[ReconstructionIteration] = Field(
        default_factory=list,
        description="Detailed log of each reconstruction iteration"
    )
    final_error: float = Field(..., description="Final reconstruction error")

    # Metadata
    reconstruction_passed: bool
    concepts_dictionary_version: str = Field(default="v1.0")

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "analysis_20240115_001",
                "timestamp": "2024-01-15T10:30:00Z",
                "board_state": "(;GM[1]FF[4]SZ[19]...)",
                "move_a": "Q16",
                "move_b": "D4",
                "vector_a": {
                    "winrate": 0.72,
                    "lead": 15.3,
                    "ownership": [],
                    "visits": 10000,
                    "move_sequence": []
                },
                "vector_b": {
                    "winrate": 0.67,
                    "lead": 10.8,
                    "ownership": [],
                    "visits": 10000,
                    "move_sequence": []
                },
                "delta_vector": {
                    "delta_winrate": 0.05,
                    "delta_lead": 4.5,
                    "delta_ownership": [],
                    "key_differences": ["Territory control", "Group safety"],
                    "magnitude": 0.08
                },
                "final_explanation": {
                    "text": "Unlike Move B (D4), Move A (Q16) prioritizes securing the upper-right corner...",
                    "version": 2,
                    "key_concepts": ["Corner value", "Joseki", "Direction of play"]
                },
                "reconstruction_attempts": 2,
                "final_error": 0.12,
                "reconstruction_passed": True,
                "concepts_dictionary_version": "v1.0"
            }
        }


class ConceptDefinition(BaseModel):
    """
    Concept from the Seminar of Theory
    Maps human terms to mathematical features
    """
    concept_name: str = Field(..., description="Human term (e.g., 'Thickness', 'Sabaki')")
    definition: str = Field(..., description="Natural language definition")
    mathematical_features: Dict[str, Tuple[float, float]] = Field(
        ...,
        description="Feature ranges (e.g., 'influence': (0.8, 1.0), 'eye_potential': (0.5, 1.0))"
    )
    examples: List[str] = Field(default_factory=list, description="Example board patterns (SGF)")
    validation_tests: List[str] = Field(
        default_factory=list,
        description="Counterfactual tests performed by Grandmaster"
    )
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in this definition")

    class Config:
        json_schema_extra = {
            "example": {
                "concept_name": "Thickness",
                "definition": "A strong, solid formation with outward-facing influence",
                "mathematical_features": {
                    "influence": [0.8, 1.0],
                    "eye_potential": [0.5, 1.0],
                    "liberties": [6.0, 999.0]
                },
                "examples": ["(;GM[1]FF[4]...)"],
                "validation_tests": ["Remove stone X -> winrate drops 8%"],
                "confidence_score": 0.85
            }
        }


class ConceptDictionary(BaseModel):
    """Complete dictionary from Seminar of Theory"""
    version: str
    concepts: List[ConceptDefinition]
    last_updated: datetime = Field(default_factory=datetime.utcnow)
