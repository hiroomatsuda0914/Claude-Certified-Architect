import anthropic

client = anthropic.Anthropic()

# ツール定義
my_tools = [{
    "name": "get_weather",
    "description": "指定した都市の天気を返す",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "都市名（例：Tokyo）"
            }
        },
        "required": ["city"]
    }
}]

# ダミーの天気取得関数
def get_weather(city):
    my_data = {
        "Tokyo": "晴れ",
        "Osaka": "曇り",
        "Kyoto": "雨"
    }
    return my_data.get(city, "天気が不明です")

# 最初のリクエスト
my_messages = [{"role": "user", "content": "東京の天気は？"}]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=256,
    tools=my_tools,
    messages=my_messages
)

print(f"stop_reason: {response.stop_reason}")


# Claudeがツール呼び出しを要求してきた場合
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
    print(f"ツール名：{tool_block.name}")
    print(f"引数：{tool_block.input}")

    my_result = get_weather(tool_block.input["city"])

    my_messages.append({"role": "assistant", "content": response.content})
    my_messages.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tool_block.id, "content": my_result}
    ]})

    final_response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        tools=my_tools,
        messages=my_messages
    )

    print(f"最終応答：{final_response.content[0].text}")