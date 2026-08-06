import anthropic

# GCPアカウントを作っていないので、このファイルは動きません

client = anthropic.AnthropicVertex(
    region = "us-east5",
    project_id = "GCP-project-id" #これは作成が必要
)

MY_MODEL = "claude-haiku-4-5@20251001"

response = client.messages.create(
    model = MY_MODEL,
    max_tokens=256,
    messages=[{"role": "user", "content": "AIに問い合わせる内容をここに書く"}],
)

print(response.content[0].text)