import anthropic

my_client = anthropic.Anthropic()

# 1. ツールの説明書。検証の順番はここにも書かない
my_tools = [
    {
        "name": "get_customer",
        "description": "顧客名から顧客IDを返す",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "顧客名"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "lookup_order",
        "description": "顧客IDから注文内容を返す",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "顧客ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "process_refund",
        "description": "顧客IDと金額で返金する",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "顧客ID"
                },
                "amount": {
                    "type": "integer",
                    "description": "返金する金額"
                }
            },
            "required": ["customer_id", "amount"]
        }
    },
]

# 2. 顧客・注文データと、それを返す関数
my_customers = {
    "田中": {"customer_id": "C-100", "name": "田中"},
}

my_orders = {
    "C-100": {"order_id": "O-555", "amount": 3000},
}


def get_customer(name):
    my_customer = my_customers.get(name)
    if my_customer is None:
        return f"{name} は登録されていません。"
    return f"顧客IDは {my_customer['customer_id']} です。"


def lookup_order(customer_id):
    my_order = my_orders.get(customer_id)
    if my_order is None:
        return f"顧客ID {customer_id} の注文はありません。"
    return f"注文IDは {my_order['order_id']}、金額は {my_order['amount']} 円です。"


def process_refund(customer_id, amount):
    print(f"    ★ Python が process_refund を実行した（customer_id={customer_id}, amount={amount}）")
    my_order = my_orders.get(customer_id)
    if my_order is None:
        return f"顧客ID {customer_id} では返金できません。"
    return f"{customer_id} に {amount} 円を返金しました。"


# 3. 検証順はシステムプロンプトに書かない。次のステップで Python が止める
my_system = """あなたはカスタマーサポートです。
注文確認や返金にはツールを使ってください。
ユーザーが名前や金額を言ったら、その値をツールの引数に使ってください。
"""


def my_ask(question):
    print(f"【あなた】{question}\n")
    my_messages = [{"role": "user", "content": question}]
    my_verified_customer_id = None

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
            print(f"【Claude】{text}")
            return

        if response.stop_reason == "tool_use":
            my_messages.append({"role": "assistant", "content": response.content})

            my_tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"【Claude】指示: {block.name}({block.input})")

                my_content = ""
                my_is_error = False

                if block.name in ("lookup_order", "process_refund") and my_verified_customer_id is None:
                    my_content = "先に get_customer で顧客を確定してください。検証済みの顧客IDがありません。"
                    my_is_error = True
                    print("    ★ Python が実行を止めた（顧客未検証）")
                elif block.name == "get_customer":
                    my_name = block.input["name"]
                    my_content = get_customer(my_name)
                    my_customer = my_customers.get(my_name)
                    if my_customer is not None:
                        my_verified_customer_id = my_customer["customer_id"]
                        print(f"    検証済みIDを保存した: {my_verified_customer_id}")
                elif block.name == "lookup_order":
                    my_content = lookup_order(my_verified_customer_id)
                elif block.name == "process_refund":
                    my_content = process_refund(
                        my_verified_customer_id,
                        block.input["amount"],
                    )
                else:
                    my_content = f"未知のツールです: {block.name}"
                    my_is_error = True

                print(f"    戻り値: {my_content}")
                my_tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": my_content,
                    "is_error": my_is_error,
                })

            my_messages.append({"role": "user", "content": my_tool_results})
            print(f"【Python】tool_result を {len(my_tool_results)} 件返した\n")

    print("周回の上限に達したので終了")


my_ask("田中です。3000円を返金してください。顧客IDには田中を使ってください。")
