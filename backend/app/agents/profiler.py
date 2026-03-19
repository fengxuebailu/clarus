"""
Agent C: The Profiler (Blind Verifier Agent)
Backbone: LLM (Gemini Pro)
Function: Reads ONLY the explanation and reconstructs the estimated vector
This is the key to the "Reconstruction Game" - validation of explanation quality
"""

import google.generativeai as genai
import json
import re
import asyncio
from typing import Dict
from ..schemas.go_analysis import ExplanationDraft, EstimatedVector
from ..core.config import settings
from .prompts import PROFILER_SYSTEM_PROMPT


class ProfilerAgent:
    """
    The Profiler - Blind Reconstruction Specialist
    Validates explanations by attempting to reconstruct numerical data from text alone
    """

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        # Don't use system_instruction to avoid compatibility issues
        self.model = genai.GenerativeModel(
            model_name=self.model_name
        )

        self.generation_config = {
            "temperature": 0.3,  # Lower temperature for more consistent reconstruction
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 256,
        }

    async def reconstruct_from_explanation(
        self,
        explanation: ExplanationDraft
    ) -> EstimatedVector:
        """
        Attempt to reconstruct the delta vector from explanation text alone
        This is the "blind test" - Profiler has no access to actual data

        Args:
            explanation: Natural language explanation from Scribe

        Returns:
            EstimatedVector with reconstructed values and confidence
        """

        prompt = f"""Read the following Go explanation and reconstruct the numerical data:

**Explanation:**
{explanation.text}

**Your Task:**
Extract the following information from the explanation above:

1. Winrate difference (delta_winrate) between Move A and Move B
2. Score lead difference (delta_lead) in points
3. Key feature shifts (what changed and by how much)
4. Your confidence level in this reconstruction

Provide your answer in the following JSON format:
```json
{{
  "winrate_estimate": <float, e.g., 0.05 for 5%>,
  "lead_estimate": <float, e.g., 4.5>,
  "key_feature_shifts": {{
    "feature_name": <float impact, 0.0 to 1.0>
  }},
  "confidence": <float, 0.0 to 1.0>
}}
```

Remember: You can ONLY use information explicitly stated in the explanation text.
"""

        try:
            # Call Gemini API in a separate thread to avoid blocking
            # NOTE: Do NOT pass generation_config - it triggers safety filter bug
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,  # Use default executor
                lambda: self.model.generate_content(
                    prompt
                )
            )

            # Parse JSON response
            reconstruction = self._parse_llm_response(response.text)

            # Ensure winrate_estimate is within valid range [0.0, 1.0]
            winrate = reconstruction.get("winrate_estimate", 0.0)
            winrate = min(1.0, max(0.0, abs(winrate)))  # Use absolute value and clamp

            return EstimatedVector(
                winrate_estimate=winrate,
                lead_estimate=abs(reconstruction.get("lead_estimate", 0.0)),  # Use absolute value
                key_feature_shifts=reconstruction.get("key_feature_shifts", {}),
                confidence=reconstruction.get("confidence", 0.5),
                explanation_used=explanation.text
            )

        except Exception as e:
            # Fallback: Try pattern matching if LLM fails
            return self._pattern_based_reconstruction(explanation)

    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse JSON from LLM response"""
        try:
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                json_str = json_match.group(0) if json_match else response_text

            return json.loads(json_str)

        except (json.JSONDecodeError, AttributeError):
            # Return default structure if parsing fails
            return {
                "winrate_estimate": 0.0,
                "lead_estimate": 0.0,
                "key_feature_shifts": {},
                "confidence": 0.3
            }

    def _pattern_based_reconstruction(self, explanation: ExplanationDraft) -> EstimatedVector:
        """
        Fallback: Use regex patterns to extract numerical values
        This is less sophisticated but provides a backup
        """

        explanation_text = explanation.text
        winrate_estimate = 0.0
        lead_estimate = 0.0
        confidence = 0.4  # Lower confidence for pattern matching

        # Pattern 1: "X% winrate" or "winrate of X%"
        winrate_pattern = r'(\d+\.?\d*)\s*%\s*(?:winrate|advantage)'
        winrate_match = re.search(winrate_pattern, explanation_text, re.IGNORECASE)
        if winrate_match:
            winrate_estimate = float(winrate_match.group(1)) / 100.0
            confidence += 0.2

        # Pattern 2: "X points" or "X point lead"
        lead_pattern = r'(\d+\.?\d*)\s*points?(?:\s+lead)?'
        lead_match = re.search(lead_pattern, explanation_text, re.IGNORECASE)
        if lead_match:
            lead_estimate = float(lead_match.group(1))
            confidence += 0.2

        # Pattern 3: "from X% to Y%" - calculate delta (use absolute value to ensure positive)
        range_pattern = r'from\s+(\d+\.?\d*)%\s+to\s+(\d+\.?\d*)%'
        range_match = re.search(range_pattern, explanation_text, re.IGNORECASE)
        if range_match:
            start = float(range_match.group(1))
            end = float(range_match.group(2))
            # Use absolute value to ensure winrate_estimate is positive
            winrate_estimate = abs(end - start) / 100.0
            confidence = max(confidence, 0.7)  # High confidence for explicit ranges

        # Extract feature shifts based on keywords
        key_feature_shifts = {}
        feature_keywords = {
            "corner": 0.0,
            "territory": 0.0,
            "thickness": 0.0,
            "influence": 0.0,
            "shape": 0.0,
            "aji": 0.0,
            "safety": 0.0
        }

        for feature in feature_keywords:
            if feature in explanation_text.lower():
                # Rough heuristic: feature mentioned = some importance
                key_feature_shifts[feature] = 0.3

        return EstimatedVector(
            winrate_estimate=winrate_estimate,
            lead_estimate=lead_estimate,
            key_feature_shifts=key_feature_shifts,
            confidence=min(confidence, 1.0),
            explanation_used=explanation_text
        )
