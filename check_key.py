import os

key = os.environ.get("OPENAI_API_KEY")

if key:
    print("✅ OPENAI_API_KEY is set")
    print("First 5 chars:", key[:5])
else:
    print("❌ OPENAI_API_KEY is NOT set")
