"""
Test script to list available Gemini models for the API key
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"Testing API key: {api_key[:10]}...")

try:
    # Configure API
    genai.configure(api_key=api_key)

    print("\n=== Available Models ===")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
            print(f"  Display name: {model.display_name}")
            print(f"  Supported methods: {model.supported_generation_methods}")
            print()

    print("=== Testing a simple generation ===")
    # Try with the simplest model name
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'hello'")
        print(f"SUCCESS with gemini-pro: {response.text}")
    except Exception as e:
        print(f"FAILED with gemini-pro: {e}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
