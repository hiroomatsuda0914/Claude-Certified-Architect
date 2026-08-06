import anthropic


# Bedrockクライアントで、リージョンを指定
client = anthropic.AnthropicBedrock(
    aws_region="us-east-1",
)

MY_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

response = client.messages.create(
    model = MY_MODEL,
    max_tokens=256,
    messages = [{"role": "user", "content": "日本の首都はどこですか"}],
)

print(response.content[0].text)
