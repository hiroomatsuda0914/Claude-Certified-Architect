import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[{"role": "user", "content": "日本語で、Write a haiku about the beauty of nature."}]
)

print(response.content[0].text)
print(response.id)
print(response.role)
print(response.usage)