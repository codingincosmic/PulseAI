import os
import json
from flask import Flask, render_template, request
from openai import OpenAI, RateLimitError
from elevenlabs.client import ElevenLabs
from datadog import statsd

app = Flask(__name__)

# ---------- Helpers ----------
def get_recent_events(limit=5):
    try:
        with open("event_stream.jsonl", "r") as f:
            lines = f.readlines()
            return [json.loads(l) for l in lines[-limit:]]
    except FileNotFoundError:
        return []

# ---------- Clients ----------
llm_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

eleven_client = ElevenLabs(
    api_key=os.environ["ELEVENLABS_API_KEY"]
)

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    audio_file = None

    if request.method == "POST":
        user_input = request.form["question"]

        # 1️⃣ LLM call with rate-limit handling
        try:
            events = get_recent_events()

            response = llm_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
User question: {user_input}

Recent system events:
{events}

Explain what is happening in simple terms.
"""
                    }
                ]
            )

            answer = response.choices[0].message.content

        except RateLimitError:
            answer = (
                "⏳ I'm getting too many requests right now. "
                "Please wait 20 seconds and try again."
            )

        # 2️⃣ Limit text for voice (Fix 1)
        MAX_VOICE_CHARS = 300
        voice_text = answer[:MAX_VOICE_CHARS]

        # 3️⃣ ElevenLabs with graceful failure (Fix 2 + Fix 3)
        try:
            audio = eleven_client.text_to_speech.convert(
                voice_id="21m00Tcm4TlvDq8ikWAM",
                text=voice_text,
                model_id="eleven_multilingual_v2"
            )

            audio_file = "static/response.mp3"
            with open(audio_file, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

        except Exception as e:
            audio_file = None
            print("Voice disabled:", e)
            statsd.increment("pulseai.voice_quota_exceeded")

    return render_template(
        "index.html",
        answer=answer,
        audio_file=audio_file
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
