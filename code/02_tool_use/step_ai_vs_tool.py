import anthropic

# 自分で定義した変数には my_ をつける（code/CLAUDE.md）
my_client = anthropic.Anthropic()

# Claude に渡すのは「説明書」だけ。この時点では関数は動かない。
my_tools = [{
    "name": "get_weather",
    "description": "指定した都市の今日の天気を返す。天気はこのツールでしか分からない。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "都市名（Tokyo または Osaka）"
            }
        },
        "required": ["city"]
    }
}]


def get_weather(city):
    """ここがツール本体。Python が実行する。Claude はこの関数の中を見られない。"""
    print("    ★ ここは Python（ツール）。Claude は止まっている")
    my_data = {
        "Tokyo": "晴れ",
        "東京": "晴れ",
        "Osaka": "曇り",
        "大阪": "曇り",
    }
    return my_data.get(city, "天気が不明です")


def my_ask(question):
    print("\n" + "=" * 40)
    print(f"【あなた】{question}")

    my_messages = [{"role": "user", "content": question}]

    # tool_choice は付けない。使うかどうかは Claude が決める（既定の auto）。
    response = my_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        tools=my_tools,
        messages=my_messages,
    )

    if response.stop_reason != "tool_use":
        text = next(b.text for b in response.content if b.type == "text")
        print("【Claude】ツールを使わず、自分で文章を書いた")
        print(f"    {text}")
        print("    ★ get_weather は呼ばれていない")
        return

    tool_block = next(b for b in response.content if b.type == "tool_use")
    print("【Claude】自分では答えられないので、ツールを呼ぶ指示だけ返した")
    print(f"    ツール名: {tool_block.name}")
    print(f"    引数: {tool_block.input}")
    print("    ※ この時点では、天気の結果はまだ無い")

    my_result = get_weather(tool_block.input["city"])
    print(f"    戻り値: {my_result}")

    # Claude の「呼んで」という指示と、Python の結果を、次の送信に載せる。
    my_messages.append({"role": "assistant", "content": response.content})
    my_messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": my_result,
        }],
    })
    print("【あなた】ツールの結果を Claude に渡した")

    final_response = my_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        tools=my_tools,
        messages=my_messages,
    )
    text = next(b.text for b in final_response.content if b.type == "text")
    print("【Claude】渡された結果を読んで、文章にした")
    print(f"    {text}")


my_ask("東京の天気は？")
my_ask("こんにちは、と短く挨拶して")
