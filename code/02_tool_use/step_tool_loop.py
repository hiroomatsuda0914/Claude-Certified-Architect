import anthropic

# 自分で定義した変数には my_ をつける（code/CLAUDE.md）
my_client = anthropic.Anthropic()

# 天気はコードがないと分からない。コードは lookup_code だけが知っている。
# そのため Claude は、最低2回ツールを呼ぶまで文章を書けない。
my_tools = [
    {
        "name": "lookup_code",
        "description": "都市名から天気コードを返す。天気を調べる前に必ず呼ぶ。コードは推測できない。",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "都市名（例：東京）"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_weather_by_code",
        "description": "lookup_code が返したコードの天気を返す。都市名では検索できない。",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "lookup_code の戻り値"}
            },
            "required": ["code"],
        },
    },
]

my_codes = {"東京": "TYO-17", "大阪": "OSA-04"}
my_weather = {"TYO-17": "晴れ", "OSA-04": "曇り"}


def lookup_code(city):
    print("    ★ Python が lookup_code を実行した")
    return my_codes.get(city, "コードが不明です")


def get_weather_by_code(code):
    print("    ★ Python が get_weather_by_code を実行した")
    return my_weather.get(code, "そのコードの天気は不明です。先に lookup_code の結果を使ってください")


def my_run_tool(name, tool_input):
    if name == "lookup_code":
        return lookup_code(tool_input["city"])
    if name == "get_weather_by_code":
        return get_weather_by_code(tool_input["code"])
    return "未知のツールです"


def my_ask(question):
    print(f"【あなた】{question}")
    print("（このあと、あなたはループの中に入りません）\n")

    my_messages = [{"role": "user", "content": question}]
    my_max_turns = 5

    for my_turn in range(1, my_max_turns + 1):
        print(f"--- 周回 {my_turn} ---")
        response = my_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system="天気を聞かれたら、lookup_code でコードを取ってから get_weather_by_code を呼ぶこと。コードを推測しないこと。",
            tools=my_tools,
            messages=my_messages,
        )

        print(f"【Python の判定】stop_reason = {response.stop_reason}")

        # 終了の判断は Claude が出した stop_reason を、Python が読んでいるだけ。
        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if b.type == "text")
            print("【Claude】必要な結果が揃ったので、文章を書いた。ここでループを抜ける")
            print(f"    {text}")
            return

        if response.stop_reason != "tool_use":
            print("想定外の stop_reason なのでループを終える")
            return

        print("【Claude】まだ答えられない。ツールを呼ぶ指示だけ返した")
        my_messages.append({"role": "assistant", "content": response.content})

        my_tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"    指示: {block.name}({block.input})")
            my_result = my_run_tool(block.name, block.input)
            print(f"    戻り値: {my_result}")
            my_tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": my_result,
            })

        my_messages.append({"role": "user", "content": my_tool_results})
        print("【Python】結果を会話に足して、次の周回へ\n")

    print("周回の上限に達したので、Python がループを止めた")


my_ask("東京の天気は？")
