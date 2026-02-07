import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ API Key missing")
    exit(1)

models = [
    "gemini/gemini-flash-latest",
    "gemini/gemini-pro-latest",
    "gemini/gemini-2.0-flash",
    "gemini/gemini-2.0-flash-exp",
    "gemini/gemini-1.5-flash", 
    "gemini/gemini-1.5-pro"
]

print("🔍 Testing Gemini Models...")

for model in models:
    print(f"\n👉 Testing: {model}")
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            api_key=api_key
        )
        print(f"✅ SUCCESS! Model '{model}' is working.")
        print(f"Response: {response.choices[0].message.content[:20]}...")
        break
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:100]}...")
