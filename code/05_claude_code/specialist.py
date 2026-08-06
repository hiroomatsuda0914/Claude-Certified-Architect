import anthropic

# ─────────────────────────────────────────
# ツール定義（オーケストレーターに渡すJSONスキーマ）
# Phase 2の weather_tool.definition と同じ構造
# ─────────────────────────────────────────

definition = {
    "name": "ask_specialist",
    "description": "指定した専門分化の専門家（Claude）に質問を転送し、回答を得る",
    "input_schema": {
        "type": "object",
        "properties": {
            "specialty": {
                "type": "string",
                "description": "専門分野（例：天気、料理など）"
            },
            "question": {
                "type": "string",
                "description": "専門家への質問内容"
            }
        },
        "required": ["specialty", "question"]
    }
}


# ─────────────────────────────────────────
# ツール実装（サブエージェント）
# Phase 2との違い：run() の中身が Claude API 呼び出し
# ─────────────────────────────────────────

def run(specialty: str, question: str) -> str:
    client = anthropic.Anthropic()
    my_system = f"あなたは{specialty}の専門家です。簡潔に2～3文で答えてください。"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens = 200,
        system = my_system,
        messages = [{"role": "user", "content": question}]
    )
    return response.content[0].text
