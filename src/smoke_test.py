from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)

resp = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Reply with exactly: harness OK"}],
    temperature=0,
)

print(resp.choices[0].message.content)
