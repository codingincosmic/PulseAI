import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain what an error spike means simply"}
    ]
)

print("✅ LLM response:")
print(response.choices[0].message.content)
