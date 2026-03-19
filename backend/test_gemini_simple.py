"""
Test if Gemini API works with a very simple prompt
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_MODEL')

print(f"API Key: {api_key[:10]}...")
print(f"Model: {model_name}")

genai.configure(api_key=api_key)

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(model_name=model_name)

# Test 1: Ultra simple
print("\n=== Test 1: Ultra simple ===")
try:
    response = model.generate_content(
        "Say hello",
        safety_settings=safety_settings
    )
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"FAILED: {e}")
    if hasattr(response, 'candidates'):
        print(f"Finish reason: {response.candidates[0].finish_reason}")

# Test 2: Mention "Go game"
print("\n=== Test 2: Mention 'Go game' ===")
try:
    response = model.generate_content(
        "Explain the rules of the Go board game in one sentence.",
        safety_settings=safety_settings
    )
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"FAILED: {e}")
    try:
        if 'response' in locals() and hasattr(response, 'candidates'):
            print(f"Finish reason: {response.candidates[0].finish_reason}")
    except:
        pass

# Test 3: Our actual prompt
print("\n=== Test 3: Our actual prompt ===")
prompt = """You are analyzing a Go game. Compare two possible moves:
- Move A: L10 (recommended by AI)
- Move B: H9 (alternative)

Please explain why Move A is better."""

try:
    response = model.generate_content(
        prompt,
        safety_settings=safety_settings
    )
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"FAILED: {e}")
    try:
        if 'response' in locals() and hasattr(response, 'candidates'):
            print(f"Finish reason: {response.candidates[0].finish_reason}")
    except:
        pass
