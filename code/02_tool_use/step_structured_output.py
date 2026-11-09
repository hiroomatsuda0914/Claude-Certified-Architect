import anthropic
import json

# 自分で定義した変数には my_ をつける（code/CLAUDE.md）
my_client = anthropic.Anthropic()

# --- 1. 取り出したい形をツールの input_schema で定義する ---
# 天気ツール（step2_tool_use.py）と同じ書き方。
# 違いは「外部APIを呼ぶ」のではなく「文章から値を抜き出す型」として使う点。
my_tools = [{
    "name": "extract_data",
    "description": "文章から人物名と点数を抽出する",
    "input_schema": {
        "type": "object",
        "properties": {
            "name" :{
                "type": "string",
                "description": "人物の名前"
            },
            "score":{
                "type": "number",
                "description": "点数"
            }
        },
        "required": ["name", "score"]
    }
}]

my_text = "田中さんは数学のテストで87点を取りました。"

my_request = {
    "model":"claude-haiku-4-5-20251001",
    "max_tokens":256,
    "tools":my_tools,
    "tool_choice": {"type": "tool", "name": "extract_data"},
    "messages": [{"role": "user", "content": my_text}],
}
print("=== リクエスト ===")
print(json.dumps(my_request, ensure_ascii=False, indent=2))
response = my_client.messages.create(**my_request)
print("=== レスポンス ===")
print(response.model_dump_json(indent=2))



# --- 2. tool_choice で、このツールを必ず呼ばせる ---
response = my_client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=my_tools,
    tool_choice = {"type": "tool", "name": "extract_data"},
    messages=[{"role": "user", "content": my_text}],
)

# --- 3. 返ってきた tool_use ブロックから値を取る ---
# ツールを実行して tool_result を返すループは、今回は不要。
# 欲しいデータは最初の応答の input に入っている。
print(f"stop_reason: {response.stop_reason}")
my_block = next(b for b in response.content if b.type == "tool_use")
my_data = my_block.input
print(f"ツール名: {my_block.name}")
print(f"input の型: {type(my_data)}")
print(f"名前: {my_data['name']}")
print(f"点数: {my_data['score']}")
