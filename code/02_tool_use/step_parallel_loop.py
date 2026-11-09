import anthropic

my_client = anthropic.Anthropic()

my_tools = [{
    "name": "get_weather",
    "description": "指定した都市の天気を返す",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "都市名（東京 または 大阪）"
            }
        },
        "required": ["city"]
    }
}]

my_weather = {
    "東京": "晴れ",
    "Tokyo": "晴れ",
    "大阪": "曇り",
    "Osaka": "曇り",
}

def get_weather(city):
    return my_weather.get(city, "天気が不明です")

def my_ask(question):
    print(f"【あなた】{question}\n")
    my_messages = [{"role": "user", "content": question}]

    for my_turn in range(1, 6):
        print(f"--- 周回 {my_turn} ---")
        response = my_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            tools=my_tools,
            messages=my_messages,
        )
        print(f"【Python の判定】stop_reason = {response.stop_reason}")

        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if b.type == "text")
            print(f"【Claude】{text}")
            return

        if response.stop_reason == "tool_use":
            my_messages.append({"role": "assistant", "content": response.content})

            my_tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"【Claude】指示: {block.name}({block.input})")
                my_result = get_weather(block.input["city"])
                print(f"    戻り値: {my_result}")
                my_tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": my_result,
                })

            my_messages.append({"role": "user", "content": my_tool_results})
            print(f"【Python】tool_result を {len(my_tool_results)} 件まとめて返した\n")

    print("周回の上限に達したので終了")

my_ask("東京と大阪の天気を教えて")
