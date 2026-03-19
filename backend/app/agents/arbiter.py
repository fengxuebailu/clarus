"""
Agent D: The Arbiter (Judge/Student Agent)
NEW MODE: Prediction-Based Verification
Function: Tests if golden_rule can guide a student to predict the correct move
"""

import math
import json
import asyncio
import re
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple
from ..schemas.go_analysis import (
    DeltaVector,
    EstimatedVector,
    ReconstructionFeedback,
    PredictionTest,
    ExplanationDraft
)
from ..core.config import settings
from .prompts import ARBITER_FEEDBACK_TEMPLATES, ARBITER_STUDENT_PROMPT
from ..utils.go_board import GoBoard, SGFParser


class ArbiterAgent:
    """
    The Arbiter - Student/Judge Agent
    NEW: Tests if golden_rule can guide prediction (prediction-based mode)
    LEGACY: Validates reconstruction quality (reconstruction-based mode)
    """

    def __init__(self, error_threshold: float = None, api_key: str = None, model: str = None):
        """
        Args:
            error_threshold: Maximum acceptable error (default from settings)
            api_key: Gemini API key for prediction mode
            model: Gemini model name for prediction mode
        """
        self.error_threshold = error_threshold or settings.RECONSTRUCTION_THRESHOLD

        # Initialize Gemini for prediction-based testing
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL

        print(f"  [Arbiter] Initializing with model: {self.model_name}")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    def judge_reconstruction(
        self,
        delta_true: DeltaVector,
        delta_estimated: EstimatedVector
    ) -> ReconstructionFeedback:
        """
        Judge whether the Profiler's reconstruction is accurate enough

        Args:
            delta_true: Ground truth delta from KataGo
            delta_estimated: Profiler's reconstruction from explanation

        Returns:
            ReconstructionFeedback with pass/fail and specific guidance
        """

        # Calculate errors
        winrate_error = abs(delta_true.delta_winrate - delta_estimated.winrate_estimate)
        lead_error = abs(delta_true.delta_lead - delta_estimated.lead_estimate)

        # Calculate combined error score (weighted average)
        # Winrate is more critical, so weight it higher
        error_score = (winrate_error * 0.7) + (lead_error / 20.0 * 0.3)

        # Generate specific feedback FIRST to check semantic quality
        feedback_text, missing_aspects = self._generate_feedback(
            delta_true,
            delta_estimated,
            winrate_error,
            lead_error
        )

        # Determine if reconstruction passed - ALIGNED LOGIC
        # If semantic checks pass (no missing aspects), be more lenient with numeric error
        if not missing_aspects:
            # Semantic quality is good, allow higher numeric error
            passed = error_score <= (self.error_threshold * 2.0)  # Double tolerance
        else:
            # Semantic quality issues, must meet strict numeric threshold
            passed = error_score <= self.error_threshold

        # Update feedback to reflect the actual decision
        if passed and not missing_aspects:
            feedback_text = (
                "[OK] APPROVED! Your explanation uses concrete tactical language, "
                "specific coordinates, and clear causal reasoning. The Profiler "
                "successfully understood the tactical consequences."
            )
        elif passed and missing_aspects:
            feedback_text = (
                "[OK] CONDITIONALLY APPROVED with minor issues:\n" + feedback_text
            )
        elif not passed:
            feedback_text = (
                "[X] REJECTED - Please revise:\n" + feedback_text
            )

        return ReconstructionFeedback(
            error_score=error_score,
            passed=passed,
            specific_feedback=feedback_text,
            missing_aspects=missing_aspects
        )

    def _generate_feedback(
        self,
        delta_true: DeltaVector,
        delta_estimated: EstimatedVector,
        winrate_error: float,
        lead_error: float
    ) -> Tuple[str, list]:
        """
        Generate SEMANTIC/CAUSAL feedback for the Scribe
        Focus on tactical reasoning quality, not numeric precision
        """

        feedback_parts = []
        missing_aspects = []

        # SEMANTIC VALIDATION - Match severity to language
        winrate_diff = abs(delta_true.delta_winrate)

        # Check if severity words match the actual impact
        if winrate_diff > 0.10:  # 10%+ is a blunder
            # MUST use severe tactical language
            if not self._contains_severity_keywords(delta_estimated.explanation_used):
                feedback_parts.append(
                    f"CRITICAL: The winrate drops by {winrate_diff * 100:.0f}%, indicating a BLUNDER. "
                    f"Your explanation uses weak words. You MUST explain the tactical DEATH, CUT, or CAPTURE. "
                    f"Find the specific group that dies or the cutting point. "
                    f"Don't say 'inefficient' or 'suboptimal' - this is a tactical disaster."
                )
                missing_aspects.append("tactical_severity")

        elif winrate_diff > 0.05:  # 5-10% is a mistake
            # Should use tactical consequence language
            if not self._contains_tactical_keywords(delta_estimated.explanation_used):
                feedback_parts.append(
                    f"The winrate drops by {winrate_diff * 100:.0f}%, indicating a clear mistake. "
                    f"You must explain the SPECIFIC tactical consequence (e.g., 'group becomes weak', "
                    f"'loses sente', 'allows invasion at X'). "
                    f"Generic words like 'less efficient' or 'suboptimal' are insufficient."
                )
                missing_aspects.append("tactical_explanation")

        # Check if CONCRETE COORDINATES are mentioned
        if not self._contains_coordinates(delta_estimated.explanation_used):
            feedback_parts.append(
                "Your explanation lacks COORDINATES. You must reference specific points "
                "(e.g., 'White will cut at Q13', 'The group at R15 dies', 'Territory at D4 is secured'). "
                "Vague regional descriptions are not enough."
            )
            missing_aspects.append("coordinate_anchoring")

        # Check if CAUSAL CHAIN is explained
        if not self._contains_causal_language(delta_estimated.explanation_used):
            feedback_parts.append(
                "Your explanation lacks CAUSAL reasoning. Explain the 'What-If' scenario: "
                "'If you play Move B, White will [PUNISHER MOVE], resulting in [CONSEQUENCE].' "
                "Don't just state that one move is better - explain WHY and WHAT HAPPENS if you don't."
            )
            missing_aspects.append("causal_chain")

        # Numeric accuracy is now SECONDARY - only check if off by >100%
        if winrate_error > (winrate_diff * 1.5) and winrate_diff > 0.03:
            feedback_parts.append(
                f"The reconstructed magnitude ({delta_estimated.winrate_estimate * 100:.0f}%) "
                f"is far from the actual ({delta_true.delta_winrate * 100:.0f}%). "
                f"While exact numbers aren't required, the ORDER OF MAGNITUDE must be correct."
            )
            missing_aspects.append("magnitude_mismatch")

        # Construct final feedback
        if not feedback_parts:
            feedback_text = (
                "Excellent! Your explanation uses concrete tactical language, "
                "specific coordinates, and clear causal reasoning. The Profiler "
                "successfully understood the tactical consequences."
            )
        else:
            feedback_text = "\n".join(feedback_parts)

        return feedback_text, missing_aspects

    def _contains_severity_keywords(self, text: str) -> bool:
        """Check if explanation contains severe tactical keywords"""
        severity_words = [
            'dead', 'dies', 'killed', 'captured', 'cut off', 'separated',
            'collapsed', 'destroyed', 'suffocated', 'crushed', 'lost',
            'catastrophic', 'disaster', 'fatal'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in severity_words)

    def _contains_tactical_keywords(self, text: str) -> bool:
        """Check if explanation contains tactical consequence keywords"""
        tactical_words = [
            'weak', 'heavy', 'cut', 'atari', 'capture', 'connect', 'separate',
            'invade', 'invasion', 'attack', 'defend', 'sente', 'gote',
            'ko', 'ladder', 'snapback', 'shortage', 'liberties'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in tactical_words)

    def _contains_coordinates(self, text: str) -> bool:
        """Check if explanation mentions specific board coordinates"""
        import re
        # Match Go coordinates like Q16, D4, etc. (letter + number)
        coord_pattern = r'\b[A-T]\d{1,2}\b'
        return bool(re.search(coord_pattern, text))

    def _contains_causal_language(self, text: str) -> bool:
        """Check if explanation contains causal/conditional language"""
        causal_words = [
            'if', 'then', 'will', 'would', 'leads to', 'results in',
            'causes', 'allows', 'prevents', 'forces', 'punish'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in causal_words)

    def calculate_final_score(
        self,
        delta_true: DeltaVector,
        delta_estimated: EstimatedVector
    ) -> Dict[str, float]:
        """
        Calculate detailed scoring metrics for analysis

        Returns:
            Dictionary with individual component scores
        """

        winrate_score = 1.0 - min(
            abs(delta_true.delta_winrate - delta_estimated.winrate_estimate) / 0.10,
            1.0
        )

        lead_score = 1.0 - min(
            abs(delta_true.delta_lead - delta_estimated.lead_estimate) / 10.0,
            1.0
        )

        # Overall reconstruction quality (0.0 to 1.0)
        overall_score = (winrate_score * 0.6) + (lead_score * 0.4)

        return {
            "winrate_accuracy": winrate_score,
            "lead_accuracy": lead_score,
            "overall_quality": overall_score,
            "profiler_confidence": delta_estimated.confidence
        }

    # ==================== BOARD RENDERING ====================

    def _render_board_text(self, board_state: str, size: int = 19) -> str:
        """
        将 SGF 转换为文本棋盘，供学生 prompt 使用。
        Render SGF board state as a text-based board for the student prompt.

        Args:
            board_state: SGF string
            size: Board size (default 19)

        Returns:
            Text representation of the board
        """
        # Initialize empty board
        board = [['.' for _ in range(size)] for _ in range(size)]

        # Parse SGF to extract moves
        try:
            parser = SGFParser(board_state)
            moves = parser.get_moves()
            size = parser.board_size

            # Re-init if size differs
            if size != 19:
                board = [['.' for _ in range(size)] for _ in range(size)]

            # Place stones (simplified - no capture logic)
            for color, gtp_coord in moves:
                try:
                    x, y = GoBoard.gtp_to_coords(gtp_coord)
                    if 0 <= x < size and 0 <= y < size:
                        board[y][x] = 'X' if color == 'B' else 'O'
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            print(f"  [Arbiter] Warning: SGF parsing failed: {e}")
            # Return a note instead of empty board
            return f"[SGF parsing failed - raw SGF: {board_state[:200]}]"

        # Render as text
        cols = GoBoard.GTP_COLS[:size]
        lines = []
        lines.append("   " + " ".join(cols))
        for row_idx in range(size):
            row_num = size - row_idx
            row_label = f"{row_num:2d}"
            row_str = " ".join(board[row_idx])
            lines.append(f"{row_label} {row_str} {row_label}")
        lines.append("   " + " ".join(cols))

        return "\n".join(lines)

    @staticmethod
    def _manhattan_distance(move1: str, move2: str) -> int:
        """
        计算两个 GTP 坐标之间的曼哈顿距离。
        Calculate Manhattan distance between two GTP coordinates.

        Returns:
            Manhattan distance, or 999 if parsing fails
        """
        try:
            x1, y1 = GoBoard.gtp_to_coords(move1)
            x2, y2 = GoBoard.gtp_to_coords(move2)
            return abs(x1 - x2) + abs(y1 - y2)
        except (ValueError, IndexError):
            return 999

    # ==================== NEW PREDICTION-BASED MODE ====================

    async def test_prediction(
        self,
        explanation: ExplanationDraft,
        board_state: str,
        move_a: str,
        move_b: str,  # NEW: need move_b for censoring too
        player_color: str
    ) -> ReconstructionFeedback:
        """
        NEW PREDICTION-BASED VERIFICATION with adjacency tolerance

        Test if the golden_rule is clear enough to guide a student to Move A.
        Adjacent predictions (Manhattan distance <= 1) count as partially correct.

        Args:
            explanation: ExplanationDraft with golden_rule
            board_state: Current board position (SGF)
            move_a: The correct move (hidden from student)
            move_b: The alternative move (also hidden)
            player_color: "B" or "W"

        Returns:
            ReconstructionFeedback with prediction test results
        """

        print(f"  [Arbiter-Student] Testing general_maxim: {explanation.general_maxim[:100]}...")

        # DEFENSIVE: Censor coordinates in both general_maxim and situation_context
        sanitized_maxim = self._censor_coordinates(explanation.general_maxim, move_a, move_b)
        sanitized_context = self._censor_coordinates(explanation.situation_context, move_a, move_b)

        if sanitized_maxim != explanation.general_maxim:
            print(f"  [Arbiter-Censor] WARNING: Censored coordinates in general_maxim!")
            print(f"  [Arbiter-Censor] Original: {explanation.general_maxim[:150]}...")

        if sanitized_context != explanation.situation_context:
            print(f"  [Arbiter-Censor] WARNING: Censored coordinates in situation_context!")

        # Construct prompt for AI student with SANITIZED maxim, context, and TEXT board
        prompt = self._construct_student_prompt(
            sanitized_maxim,
            sanitized_context,
            board_state,
            player_color
        )

        try:
            # Call Gemini API to predict move
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    prompt,
                    safety_settings=self.safety_settings
                )
            )

            # Defensive: Check if response has text
            if not response or not hasattr(response, 'text') or response.text is None:
                raise ValueError("Gemini API returned no text content")

            response_text = response.text.strip()

            # Parse JSON response
            try:
                if response_text.startswith('```json'):
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                elif response_text.startswith('```'):
                    response_text = response_text.split('```')[1].split('```')[0].strip()

                parsed = json.loads(response_text)
                predicted_move = parsed.get('predicted_move', '').strip().upper()
                reasoning = parsed.get('reasoning', '')

            except json.JSONDecodeError:
                # Fallback: extract first coordinate-like pattern
                match = re.search(r'\b([A-T]\d{1,2})\b', response_text)
                predicted_move = match.group(1).upper() if match else "UNKNOWN"
                reasoning = response_text[:200]

            # Compare prediction with correct move (with adjacency tolerance)
            correct_move = move_a.strip().upper()
            exact_match = (predicted_move == correct_move)
            distance = self._manhattan_distance(predicted_move, correct_move)
            partially_correct = (not exact_match) and (distance <= 1)

            # Create PredictionTest result
            prediction_test = PredictionTest(
                predicted_move=predicted_move,
                correct_move=correct_move,
                prediction_correct=exact_match or partially_correct,
                reasoning=reasoning
            )

            # Generate feedback
            if exact_match:
                feedback_text = (
                    f"[OK] 通过！学生根据你的格言正确预测了 {predicted_move}。\n\n"
                    f"学生的推理：{reasoning[:200]}\n\n"
                    f"你的格言清晰且可操作！"
                )
                passed = True
                missing_aspects = []
            elif partially_correct:
                feedback_text = (
                    f"[~] 基本通过！学生预测了 {predicted_move}，"
                    f"与正解 {correct_move} 相邻（距离：{distance}）。\n\n"
                    f"学生的推理：{reasoning[:200]}\n\n"
                    f"学生找到了正确的区域但未精确到点位。"
                    f"你的格言成功引导到了正确区域——视为通过。"
                )
                passed = True
                missing_aspects = []
                print(f"  [Arbiter-Student] Adjacent match! {predicted_move} is {distance} step(s) from {correct_move}")
            else:
                # FAILURE CASE: Ask student to analyze concept gap
                print(f"  [Arbiter-Student] Prediction failed (distance: {distance}). Asking student to analyze concept gap...")

                concept_gap_analysis = await self._analyze_concept_gap(
                    sanitized_maxim,
                    predicted_move,
                    correct_move,
                    reasoning,
                    board_state,
                    player_color
                )

                feedback_text = (
                    f"未通过！学生预测了 {predicted_move}，"
                    f"但正解是 {correct_move}（距离：{distance}）。\n\n"
                    f"概念偏差分析：\n{concept_gap_analysis}\n\n"
                    f"修改指导：\n"
                    f"请调整格言的用词和描述，纠正上述理解偏差。"
                    f"重点说清 {correct_move} 和 {predicted_move} 在战术上的区别。"
                )
                passed = False
                missing_aspects = ["concept_gap"]

            print(f"  [Arbiter-Student] Prediction: {predicted_move} (correct: {correct_move}) - {'PASS' if passed else 'FAIL'}")

            return ReconstructionFeedback(
                prediction_test=prediction_test,
                passed=passed,
                specific_feedback=feedback_text,
                error_score=0.0 if passed else 1.0,
                missing_aspects=missing_aspects
            )

        except Exception as e:
            print(f"  [Arbiter-Student] ERROR: {e}")
            # Return error state - don't mark as passed
            prediction_test = PredictionTest(
                predicted_move="ERROR",
                correct_move=move_a,
                prediction_correct=False,
                reasoning=f"Error during prediction: {str(e)}"
            )

            return ReconstructionFeedback(
                prediction_test=prediction_test,
                passed=False,  # Technical error should not be treated as success
                specific_feedback=f"Technical error occurred: {str(e)}. Please try again.",
                error_score=1.0,
                missing_aspects=["technical_error"]
            )

    def _censor_coordinates(self, text: str, move_a: str, move_b: str) -> str:
        """
        ANTI-CHEATING: Remove explicit coordinates from golden_rule

        Replaces:
        - Move A coordinates (e.g., "D11") → "[Target Move]"
        - Move B coordinates (e.g., "D4") → "[Alternative Move]"
        """
        import re

        # Sanitize input coordinates
        move_a_upper = move_a.strip().upper()
        move_b_upper = move_b.strip().upper()

        # Replace Move A (case-insensitive, word boundary)
        sanitized = re.sub(
            rf'\b{re.escape(move_a_upper)}\b',
            '[Target Move]',
            text,
            flags=re.IGNORECASE
        )

        # Replace Move B
        sanitized = re.sub(
            rf'\b{re.escape(move_b_upper)}\b',
            '[Alternative Move]',
            sanitized,
            flags=re.IGNORECASE
        )

        return sanitized

    async def _analyze_concept_gap(
        self,
        general_maxim: str,
        predicted_move: str,
        correct_move: str,
        reasoning: str,
        board_state: str,
        player_color: str
    ) -> str:
        """
        Ask the Student to analyze why they guessed wrong
        Returns a detailed concept gap analysis
        """

        gap_prompt = f"""你是刚才猜错的学生，现在已经知道正确答案了。请分析你的理解偏差。

**情况：**
- 老师的格言："{general_maxim}"
- 你的预测：{predicted_move}
- 正确答案：{correct_move}
- 你的推理：{reasoning}

**请分析以下三个问题：**

1. **你理解错了什么？**
   - 是误解了术语（比如把"压"理解成了"接"）？
   - 是看错了棋盘区域？
   - 是判断错了紧急程度（选了不紧急的地方）？

2. **比较两手棋的差别：**
   - {predicted_move} 在棋盘什么位置？想达成什么目的？
   - {correct_move} 在棋盘什么位置？实际达成什么效果？
   - 两者的战术区别是什么？

3. **格言应该怎么改？**
   - 用什么词汇才能引导你找到正确的位置？
   - 缺少了什么棋型描述？

**输出格式（纯文本，3-5句话）：**
示例："我预测了C14，因为格言说'头上一压'，我以为是攻击对方的棋子。但正解R13其实是防守断点的'接'。格言应该说'防断点'而不是'压'。另外紧急程度不够明确——应该强调这是死活问题。"

请具体、尖锐地指出问题。你的反馈会帮助老师修改格言。"""

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    gap_prompt,
                    safety_settings=self.safety_settings
                )
            )

            # Defensive: Check if response has text
            if not response or not hasattr(response, 'text') or response.text is None:
                raise ValueError("Gemini API returned no text content")

            analysis = response.text.strip()
            return analysis

        except Exception as e:
            print(f"  [Arbiter-Gap] ERROR analyzing concept gap: {e}")
            return f"Unable to analyze concept gap (error: {str(e)}). The predicted move {predicted_move} differs from the correct move {correct_move}."

    def _construct_student_prompt(
        self,
        general_maxim: str,
        situation_context: str,
        board_state: str,
        player_color: str
    ) -> str:
        """Construct prompt for AI student prediction test with rendered board"""

        # Render text board from SGF
        board_text = self._render_board_text(board_state)
        color_name = "黑棋 (Black)" if player_color == "B" else "白棋 (White)"

        prompt = ARBITER_STUDENT_PROMPT + "\n\n"

        prompt += f"""**本次测试输入 Input for This Test：**

老师的局面描述 Situation Context：
"{situation_context}"

老师的格言 General Maxim：
"{general_maxim}"

当前轮到：{color_name}

棋盘状态 Board State：
```
{board_text}
```

**解题步骤：**
1. 先读局面描述，理解老师在说棋盘的哪个局部
2. 在棋盘上找到对应的局部
3. 再读格言，理解应该在这个局部怎么下
4. 如果格言中出现 "[Target Move]" 这样的占位符，说明坐标被审查了，请忽略
5. 用中文推理，坐标用 GTP 格式（如 Q16、D4）

**请输出（必须是合法 JSON）：**
```json
{{
  "predicted_move": "Q16",
  "reasoning": "用中文解释：(1) 局面描述指向了棋盘的哪个区域，(2) 你在那里找到了什么棋型，(3) 根据格言为什么选这手棋"
}}
```"""

        return prompt
