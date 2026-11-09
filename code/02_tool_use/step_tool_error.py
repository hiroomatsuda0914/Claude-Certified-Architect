import anthropic

# 自分で定義した変数には my_ をつける（code/CLAUDE.md）
my_client = anthropic.Anthropic()

# 在庫を知っているのはこの関数だけ。商品名では検索できない。
my_tools = [{
    "name": "get_stock",
    "description": "SKU で在庫数を返す。商品名では検索できない。",
    "input_schema": {
        "type": "object",
        "properties": {
            "sku": {
                "type": "string",
                "description": "商品の SKU"
            }
        },
        "required": ["sku"],
    },
}]

my_stock = {"PEN-01": "12"}


def get_stock(sku):
    print(f"    ★ Python が get_stock を実行した（sku={sku}）")
    if sku in my_stock:
        return my_stock[sku], False
    if sku == "ボールペン":
        return "商品名では検索できません。SKU は PEN-01 です。", True
    return f"SKU {sku} は存在しません。", True


my_system = """あなたは在庫係です。
在庫を聞かれたら get_stock を使ってください。
最初の1回は、ユーザーが言った商品名をそのまま sku に入れてください。
ツール結果の is_error が true のときは失敗です。本文に SKU があれば、その SKU で1回だけ再試行してください。
再試行でも失敗したら、在庫は不明だと伝えて終了してください。
"""


def my_ask(question):
    print(f"【あなた】{question}\n")
    my_messages = [{"role": "user", "content": question}]

    for my_turn in range(1, 6):
        print(f"--- 周回 {my_turn} ---")
        response = my_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system=my_system,
            tools=my_tools,
            messages=my_messages,
        )
        print(f"【Python の判定】stop_reason = {response.stop_reason}")

        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if b.type == "text")
            print("【Claude】これ以上ツールは不要と判断し、文章を書いた")
            print(f"    {text}")
            return

        if response.stop_reason != "tool_use":
            print("想定外の stop_reason なので終了")
            return

        my_messages.append({"role": "assistant", "content": response.content})
        my_tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"【Claude】指示: {block.name}({block.input})")
            my_content, my_is_error = get_stock(block.input["sku"])
            my_tool_result = {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": my_content,
                "is_error": my_is_error,
            }
            print(f"    戻り値: {my_content}")
            print(f"    is_error: {my_is_error}")
            my_tool_results.append(my_tool_result)

        my_messages.append({"role": "user", "content": my_tool_results})
        if any(result["is_error"] for result in my_tool_results):
            print("【Python】失敗を隠さず Claude に返した。やり直し方は決めていない\n")
        else:
            print("【Python】成功した結果を Claude に返した\n")

    print("周回の上限に達したので終了")


my_ask("ボールペンの在庫は？")
