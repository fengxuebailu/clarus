"""
Agent B: The Scribe (Explainer Agent)
Backbone: LLM (Gemini Pro)
Function: Translates data differences (ΔV) into Natural Language Explanations
Constraint: Must use specific Go terminology from Concept Dictionary
"""

import google.generativeai as genai
from typing import Dict, List, Optional
from ..schemas.go_analysis import DeltaVector, ExplanationDraft
from ..core.config import settings
from .prompts import SCRIBE_SYSTEM_PROMPT
from ..utils.pro_games import get_few_shot_examples, get_reference_by_concept
import json
import asyncio


class ScribeAgent:
    """
    The Scribe - Natural Language Explainer
    Converts mathematical deltas into human-understandable Go wisdom
    """

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL

        # Debug: Print what model we're using
        print(f"  [Scribe] Initializing with model: {self.model_name}")
        print(f"  [Scribe] API key: {self.api_key[:10]}...")

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        # Don't use system_instruction to avoid safety filter issues
        self.model = genai.GenerativeModel(
            model_name=self.model_name
        )

        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 512,
        }

        # Safety settings - set to BLOCK_NONE for technical Go analysis
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    async def generate_explanation(
        self,
        delta_vector: DeltaVector,
        move_a: str,
        move_b: str,
        player_color: str,
        version: int = 1,
        feedback: str = None,
        punisher_sequence: List[str] = None,
        board_state: str = None,
        learned_principles: List[Dict] = None
    ) -> ExplanationDraft:
        """
        Generate natural language explanation from delta vector

        Args:
            delta_vector: Mathematical differences between moves
            move_a: AI's best move (e.g., "Q16")
            move_b: Alternative move (e.g., "D4")
            player_color: "B" or "W"
            version: Explanation version number (T_1, T_2, etc.)
            feedback: Optional feedback from previous iteration
            punisher_sequence: Opponent's best response to Move B (from KataGo PV)

        Returns:
            ExplanationDraft with natural language explanation
        """

        # Construct the prompt for LLM
        prompt = self._construct_prompt(
            delta_vector,
            move_a,
            move_b,
            player_color,
            feedback,
            punisher_sequence,
            board_state,
            learned_principles
        )

        # Debug: Log feedback status
        if feedback:
            print(f"  [Scribe] Using feedback from previous attempt (length: {len(feedback)} chars)")
        else:
            print(f"  [Scribe] No feedback - first attempt")

        # Debug: Print prompt length (full prompt omitted to avoid encoding issues)
        print(f"  [Scribe] Prompt length: {len(prompt)} chars")

        try:
            # Call Gemini API in a separate thread to avoid blocking the async event loop
            # NOTE: Do NOT pass generation_config - it triggers safety filter bug
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,  # Use default executor
                lambda: self.model.generate_content(
                    prompt,
                    safety_settings=self.safety_settings
                )
            )

            response_text = response.text.strip()

            # Parse JSON response
            try:
                # Remove markdown code blocks if present
                if response_text.startswith('```json'):
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                elif response_text.startswith('```'):
                    response_text = response_text.split('```')[1].split('```')[0].strip()

                # Strategy 1: Try direct parsing with strict=False
                parsed = None
                try:
                    parsed = json.loads(response_text, strict=False)
                except json.JSONDecodeError:
                    # Strategy 2: Try to extract and parse JSON object using regex
                    import re
                    # Find JSON object pattern
                    json_match = re.search(r'\{[\s\S]*\}', response_text)
                    if json_match:
                        try:
                            json_str = json_match.group(0)
                            # Remove any control characters within string values
                            # This is a simplified approach - replace common control chars
                            json_str = json_str.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                            parsed = json.loads(json_str, strict=False)
                        except:
                            pass

                if parsed:
                    return ExplanationDraft(
                        situation_context=parsed.get('situation_context', ''),
                        general_maxim=parsed.get('general_maxim', ''),
                        detailed_analysis=parsed.get('detailed_analysis', ''),
                        version=version,
                        key_concepts=parsed.get('key_concepts', [])
                    )
                else:
                    # Strategy 3: Use regex to extract fields directly
                    import re
                    sit_match = re.search(r'"situation_context"\s*:\s*"([^"]+)"', response_text)
                    max_match = re.search(r'"general_maxim"\s*:\s*"([^"]+)"', response_text)
                    det_match = re.search(r'"detailed_analysis"\s*:\s*"([^"]+)"', response_text)

                    situation = sit_match.group(1) if sit_match else "[Parse failed]"
                    maxim = max_match.group(1) if max_match else response_text[:200]
                    detailed = det_match.group(1) if det_match else response_text

                    concepts = self._extract_concepts(response_text)
                    print(f"  [Scribe] Used regex extraction fallback")
                    return ExplanationDraft(
                        situation_context=situation,
                        general_maxim=maxim,
                        detailed_analysis=detailed,
                        version=version,
                        key_concepts=concepts
                    )

            except Exception as parse_err:
                print(f"  [Scribe] All JSON parsing strategies failed: {parse_err}")
                print(f"  [Scribe] Raw response: {response_text[:300]}...")
                # Last resort - try regex extraction from raw text even if JSON parsing threw exception
                import re
                sit_match = re.search(r'"situation_context"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text)
                max_match = re.search(r'"general_maxim"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text)
                det_match = re.search(r'"detailed_analysis"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text)

                situation = sit_match.group(1) if sit_match else "[Parsing error]"
                maxim = max_match.group(1) if max_match else response_text[:200]
                detailed = det_match.group(1) if det_match else response_text

                # Strip any leftover JSON artifacts from maxim
                if maxim.startswith('{') or maxim.startswith('"'):
                    maxim = re.sub(r'^[\{\"\s]+', '', maxim)
                    maxim = re.sub(r'[\}\"\s]+$', '', maxim)

                concepts = self._extract_concepts(response_text)
                print(f"  [Scribe] Used last-resort regex extraction. Maxim: {maxim[:80]}...")
                return ExplanationDraft(
                    situation_context=situation,
                    general_maxim=maxim,
                    detailed_analysis=detailed,
                    version=version,
                    key_concepts=concepts
                )

        except Exception as e:
            # Fallback to template-based explanation if LLM fails
            print(f"  [Scribe] ERROR: Gemini API call failed: {type(e).__name__}: {str(e)}")

            # Debug: Try to get safety ratings if available
            try:
                if 'response' in locals() and hasattr(response, 'candidates') and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    print(f"  [Scribe] Finish reason: {candidate.finish_reason}")
                    if hasattr(candidate, 'safety_ratings'):
                        print(f"  [Scribe] Safety ratings:")
                        for rating in candidate.safety_ratings:
                            print(f"    - {rating.category}: {rating.probability}")
            except Exception as debug_error:
                print(f"  [Scribe] Debug info unavailable: {debug_error}")

            print(f"  [Scribe] Using fallback template explanation")
            return self._generate_fallback_explanation(
                delta_vector,
                move_a,
                move_b,
                version
            )

    def _construct_prompt(
        self,
        delta_vector: DeltaVector,
        move_a: str,
        move_b: str,
        player_color: str,
        feedback: str = None,
        punisher_sequence: List[str] = None,
        board_state: str = None,
        learned_principles: List[Dict] = None
    ) -> str:
        """Construct the prompt for the LLM - 变化图推演教学法"""

        # Determine opponent color
        opponent_color = "W" if player_color == "B" else "B"
        color_name = "黑棋" if player_color == "B" else "白棋"
        opp_color_name = "白棋" if player_color == "B" else "黑棋"

        # Start with system prompt
        prompt = SCRIBE_SYSTEM_PROMPT + "\n\n"

        # Inject student's knowledge base (基础棋理 + 已学棋理)
        prompt += self._build_knowledge_context(
            delta_vector.key_differences,
            learned_principles
        )

        # Add board state if available
        if board_state:
            prompt += f"""**当前棋局 SGF 记录（Current Board State）：**
请仔细阅读以下 SGF，理解棋盘上每颗棋子的位置，据此分析局面。

```
{board_state}
```

"""

        # Add input data
        prompt += f"""**本局输入数据 Input Data：**

当前轮到{color_name}（{player_color}）落子。

```json
{{
  "move_a_正解": "{move_a}",
  "move_b_错手": "{move_b}",
  "player_color": "{player_color}",
  "delta_vector": {{
    "delta_winrate": {delta_vector.delta_winrate:.4f},
    "delta_lead": {delta_vector.delta_lead:.2f},
    "key_differences": {json.dumps(delta_vector.key_differences, ensure_ascii=False)}
  }},
  "punisher_sequence_惩罚变化": {json.dumps(punisher_sequence[:10] if punisher_sequence else [], ensure_ascii=False)}
}}
```

**你的任务：**
用变化图推演教学法，生成一个 JSON 响应：
1. **situation_context**：描述当前局面的关键矛盾（不用坐标）
2. **general_maxim**：可迁移的棋理格言（像老师复盘时说的话，不要套公式）
3. **detailed_analysis**：完整战术分析（可以用坐标，展示惩罚变化和正解的妙处）
4. **key_concepts**：涉及的围棋概念列表

**记住：** general_maxim 会被单独交给学生测试，学生只看到棋盘和格言，必须能据此找到正解。"""

        if feedback:
            prompt += f"""

**上一次的学生反馈 Feedback from Previous Attempt：**
{feedback}

**修改指导（根据学生的失败模式）：**
"""
            # 棋型识别失败：学生看到了错误的棋型
            if self._is_direction_error(feedback):
                prompt += """- ⚠️ **棋型混淆**：学生在棋盘上认错了棋型！
- 你的格言描述的棋型特征不够独特，学生在别的地方也找到了类似的形状
- 补充这个棋型的**独有特征**：比如"这个断点旁边对方已经有子盯着"比单说"有断点"更精确
- 用后果的严重程度区分：如果有多个类似棋型，说清哪个的后果更致命
"""
            # 精度不足：学生找对了区域但位置偏了
            if self._is_depth_error(feedback):
                prompt += """- ⚠️ **精度不足**：学生找对了区域但具体位置偏了！
- 用棋子之间的**形状关系**来锚定位置（如"在对方两颗子的空隙处""在对方棋子的肩上"）
- 解释为什么这个精确位置比旁边几路更好（如"低一路会被封住""高一路太轻对方不怕"）
"""
            # 多候选混淆：学生找到了多个符合描述的位置
            if self._is_ambiguity_error(feedback):
                prompt += """- ⚠️ **多候选混淆**：学生在棋盘上找到了多个符合格言的位置！
- 你的 situation_context 没有帮学生消歧
- 在 situation_context 中描述目标局部的**独有特征**：它和其他类似局部有什么不同？
- 例如："这个角的外墙中间少了一手，另一个角的外墙是连续的，不需要打入"
"""
            # 通用指导（总是包含）
            prompt += """- 仔细阅读学生的反馈，理解他把哪个棋型看成了正解
- situation_context 负责帮学生定位到正确的局部，general_maxim 负责教棋理
- 问自己：学生读了 situation_context 后能不能找到我说的那个局部？"""

        prompt += """

**输出格式（必须是合法 JSON）：**
```json
{
  "situation_context": "描述目标局部的独有特征，帮学生在棋盘上定位。可以用方位词但不用坐标。如果有多个类似局部，说清区别",
  "general_maxim": "可迁移的棋理格言：描述棋型特征和战术逻辑，不用坐标也不用方位词",
  "detailed_analysis": "完整战术分析，使用坐标，展示错手惩罚和正解好处",
  "key_concepts": ["急所", "断点", "厚薄"]
}
```"""

        return prompt

    def _build_knowledge_context(
        self,
        key_differences: List[str],
        learned_principles: List[Dict] = None
    ) -> str:
        """
        构建学生的知识背景：基础棋理 + 已学棋理
        让 Scribe 知道学生已经懂什么，可以在此基础上递进教学
        """
        context = ""

        # 1. 基础棋理（pro_games 中与当前局面概念相关的条目）
        relevant_basics = []
        concept_keywords = ["断点", "打入", "三三", "肩冲", "封锁", "弃子", "对杀",
                           "厚薄", "先手", "模样", "守角", "转换"]
        for kw in concept_keywords:
            for diff in key_differences:
                if kw in diff:
                    refs = get_reference_by_concept(kw)
                    for ref in refs:
                        if ref.title not in [r.title for r in relevant_basics]:
                            relevant_basics.append(ref)

        if relevant_basics:
            context += "**学生的基础知识（已学过的棋理，可以引用）：**\n\n"
            for ref in relevant_basics[:3]:  # 最多3条，避免 prompt 太长
                context += f"- **{ref.title}**：{ref.principle[:100]}...\n"
            context += '\n你可以在格言中引用这些已学概念，例如"和\'点三三侵入时机\'的道理一样……"\n\n'

        # 2. 已学棋理（用户之前的教学记录）
        if learned_principles:
            context += "**学生之前学过的棋理（近期课堂笔记）：**\n\n"
            for p in learned_principles[:5]:  # 最多5条
                maxim = p.get("general_maxim", "")
                concepts = p.get("key_concepts", [])
                if maxim:
                    context += f"- {maxim[:80]}... (概念: {', '.join(concepts[:3])})\n"
            context += "\n如果当前局面和之前学过的棋理有关联，可以建立联系：'上次我们学了X，这次的局面虽然不同，但道理类似……'\n\n"

        return context

    def _is_direction_error(self, feedback: str) -> bool:
        """检测反馈是否表明棋型混淆（学生在错误区域找到了类似棋型）"""
        import re
        distance_match = re.search(r'距离[：:]\s*(\d+)', feedback)
        if distance_match and int(distance_match.group(1)) >= 8:
            return True
        direction_keywords = ['看错了棋盘区域', '错误的方向', '错误的区域', '看错了区域', '另一边']
        return any(kw in feedback for kw in direction_keywords)

    def _is_depth_error(self, feedback: str) -> bool:
        """检测反馈是否表明精度不足（找对区域但位置偏了）"""
        import re
        distance_match = re.search(r'距离[：:]\s*(\d+)', feedback)
        if distance_match:
            dist = int(distance_match.group(1))
            if 2 <= dist <= 7:
                return True
        depth_keywords = ['方向对了', '接近但', '偏了', '太高', '太低', '太深', '太浅']
        return any(kw in feedback for kw in depth_keywords)

    def _is_ambiguity_error(self, feedback: str) -> bool:
        """检测是否因为多候选混淆导致失败"""
        keywords = ['多个', '另一个', '也有', '类似', '混淆', '区分不了', '好几个', '候选']
        return any(kw in feedback for kw in keywords)

    def _extract_concepts(self, explanation_text: str) -> List[str]:
        """
        Extract Go concepts mentioned in the explanation
        This helps track which terminology is being used
        """
        go_concepts = [
            "Thickness", "厚み",
            "Aji", "味",
            "Shape", "形",
            "Sabaki", "捌き",
            "Kiai", "気合",
            "Miai", "見合い",
            "Sente", "先手",
            "Gote", "後手",
            "Joseki", "定石",
            "Fuseki", "布石",
            "Tesuji", "手筋",
            "Ko", "コウ",
            "Influence", "勢力",
            "Territory", "地",
            "Corner", "隅",
            "Side", "辺",
            "Center", "中央"
        ]

        found_concepts = []
        for concept in go_concepts:
            if concept.lower() in explanation_text.lower():
                found_concepts.append(concept)

        return list(set(found_concepts))  # Remove duplicates

    def _generate_fallback_explanation(
        self,
        delta_vector: DeltaVector,
        move_a: str,
        move_b: str,
        version: int
    ) -> ExplanationDraft:
        """
        Generate a template-based explanation if LLM fails
        This ensures the system always produces output
        """

        winrate_pct = delta_vector.delta_winrate * 100
        lead_pts = delta_vector.delta_lead

        situation_context = f"The position involves comparing two moves: {move_a} and {move_b}."

        general_maxim = f"Prioritize moves that provide both immediate winrate advantage and solid positional value."

        detailed_analysis = f"""Unlike Move B ({move_b}), Move A ({move_a}) provides a winrate advantage of {winrate_pct:.2f}% and increases the score lead by {lead_pts:.2f} points.

The primary difference stems from {delta_vector.key_differences[0] if delta_vector.key_differences else 'positional value'}. Move A demonstrates superior efficiency in the current position, creating a more solid foundation for future play.

From a whole-board perspective, this move choice reflects modern AI opening theory, which prioritizes immediate value over potential development."""

        return ExplanationDraft(
            situation_context=situation_context,
            general_maxim=general_maxim,
            detailed_analysis=detailed_analysis,
            version=version,
            key_concepts=["Territory", "Shape", "Efficiency"]
        )
