import anthropic
import datetime_tool
import json

client = anthropic.Anthropic()

def log(title, data):
    """通信内容を見やすく表示するヘルパー関数"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(json.dumps(data, ensure_ascii=False, indent=2))

# ─────────────────────────────────────────
# 自分で定義するもの（my_ 接頭辞）
# ─────────────────────────────────────────
my_tools = [datetime_tool.definition]                        # [] = リスト。ツールは複数渡せるのでリスト形式
my_messages = [{"role": "user", "content": "今から45分後は、何時ですか？"}]  # [] = リスト。{} = 辞書（1メッセージ = 1辞書）

# ─────────────────────────────────────────
# 【1回目の送信】Claudeにメッセージとツール定義を送る
# ─────────────────────────────────────────
log("送信① my_messages", my_messages)
log("送信① my_tools", my_tools)

response = client.messages.create(      # ← ここでHTTPリクエストが飛ぶ（サーバーとの通信①）
    model="claude-haiku-4-5",
    max_tokens=300,
    tools=my_tools,                     # 自分で定義したツール定義を渡す
    messages=my_messages,               # 自分で定義したメッセージを渡す
    )
# response はAPIから返ってくるオブジェクト（自分では定義しない）

log("受信① response.content", [b.model_dump() for b in response.content])
print(f"\n  stop_reason: {response.stop_reason}")

# ─────────────────────────────────────────
# Claudeがツール呼び出しを要求してきた場合
# ─────────────────────────────────────────
if response.stop_reason == "tool_use":  # response.stop_reason はAPIから来た値
    # response.content はAPIから来たブロックのリスト
    # tool_block はその中のtool_useブロック（APIから来たオブジェクト）
    tool_block = next(b for b in response.content if b.type == "tool_use")

    if tool_block.name == "get_current_datetime":            # tool_block.name はAPIから来た値
        my_result = datetime_tool.run()
        # my_result は自分のコードが実行した結果

    print(f"\n  [ローカル実行] datetime_tool.run() → {my_result}")

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
    log("送信② my_messages[-1]（tool_result）", my_messages[-1])

    final_response = client.messages.create(    # ← ここでHTTPリクエストが飛ぶ（サーバーとの通信②）
        model="claude-haiku-4-5",
        max_tokens=300,
        tools=my_tools,
        messages=my_messages,                   # tool_result が追加済みのリスト
        )
    # final_response はAPIから返ってくるオブジェクト

    log("受信② final_response.content", [b.model_dump() for b in final_response.content])
    print(f"\n{'='*50}")
    print(f"  最終応答: {final_response.content[0].text}")
    print(f"{'='*50}\n")
    #        ↑ final_response.content はAPIから来た値