import os

key = os.environ.get("ELEVENLABS_API_KEY")

if key:
    print("✅ ELEVENLABS_API_KEY is set")
    print("First 4 chars:", key[:4])
else:
    print("❌ ELEVENLABS_API_KEY is NOT set")
