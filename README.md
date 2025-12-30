# PulseAI

PulseAI is a real-time AI observability system that explains live system behavior in plain language.

## 🚀 What It Does
- Ingests real-time system events
- Uses AI to summarize system health
- Highlights failures like payment errors
- Degrades gracefully when services hit limits

## 🧠 Why It Matters
Modern systems produce massive logs and metrics. PulseAI reduces cognitive load by turning system noise into clear explanations.

## 🛠 Tech Stack
- Python, Flask
- OpenAI (LLM reasoning)
- ElevenLabs (voice, optional)
- Event-driven architecture
- Datadog (observability)

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
python event_producer.py
ddtrace-run python app.py
