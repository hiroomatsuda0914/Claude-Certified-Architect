import anthropic
import weather_tool

client = anthropic.Anthropic()

# ─────────────────────────────────────────
# 自分で定義するもの（my_ 接頭辞）
# ─────────────────────────────────────────
my_tools = [weather_tool.definition]                        # [] = リスト。ツールは複数渡せるのでリスト形式
my_messages = [{"role": "user", "content": "東京の天気は?"}]  # [] = リスト。{} = 辞書（1メッセージ = 1辞書）

# ─────────────────────────────────────────
# 【1回目の送信】Claudeにメッセージとツール定義を送る
# ─────────────────────────────────────────
response = client.messages.create(      # ← ここでHTTPリクエストが飛ぶ（サーバーとの通信①）
    model="claude-haiku-4-5",
    max_tokens=300,
    tools=my_tools,                     # 自分で定義したツール定義を渡す
    messages=my_messages,               # 自分で定義したメッセージを渡す
    )
# response はAPIから返ってくるオブジェクト（自分では定義しない）

# ─────────────────────────────────────────
# Claudeがツール呼び出しを要求してきた場合
# ─────────────────────────────────────────
if response.stop_reason == "tool_use":  # response.stop_reason はAPIから来た値
    # response.content はAPIから来たブロックのリスト
    # tool_block はその中のtool_useブロック（APIから来たオブジェクト）
    tool_block = next(b for b in response.content if b.type == "tool_use")

    if tool_block.name == "get_weather":            # tool_block.name はAPIから来た値
        my_result = weather_tool.run(
            tool_block.input["city"]                # tool_block.input はAPIから来た値（Claudeが決めた引数）
        )
        # my_result は自分のコードが実行した結果

    # ── 会話履歴にClaudeの返答（tool_useブロック）を追加 ──
    my_messages.append({"role": "assistant", "content": response.content})
    #                                                       ↑ APIから来たブロックをそのまま追加

    # ── tool_result を組み立てて追加 ──
    my_messages.append({"role": "user", "content":[    # content の値は [] リスト
        {                                               # {} = tool_result ブロック（辞書）
            "type": "tool_result",          # 固定値（自分で書く）
            "tool_use_id": tool_block.id,   # tool_block.id はAPIから来た値（紐付け用ID）
            "content": my_result            # 自分のコードが実行した結果
        }
    ]})

    # ─────────────────────────────────────────
    # 【2回目の送信】tool_result を渡してClaudeに最終回答を生成させる
    # ─────────────────────────────────────────
    final_response = client.messages.create(    # ← ここでHTTPリクエストが飛ぶ（サーバーとの通信②）
        model="claude-haiku-4-5",
        max_tokens=300,
        tools=my_tools,
        messages=my_messages,                   # tool_result が追加済みのリスト
        )
    # final_response はAPIから返ってくるオブジェクト

    print(f"最終応答: {final_response.content[0].text}")
    #                   ↑ final_response.content はAPIから来た値