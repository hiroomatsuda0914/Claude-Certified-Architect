import anthropic
import weather_tool
import datetime_tool

client = anthropic.Anthropic()

def run_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return weather_tool.run(tool_input["city"])
    elif tool_name == "get_current_datetime":
        return datetime_tool.run()
    
    
print("=== パート1: 並列ツール呼び出し ===\n")

my_tools = [weather_tool.definition, datetime_tool.definition]
my_messages = [
      {"role": "user", "content": "東京と大阪の天気を同時に教えてください。今の時刻も合わせてお願いします。"}
]

response = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 1024,
    tools = my_tools,
    messages = my_messages
)

print(f"stop_reason: {response.stop_reason}")
print(f"tool_use ブロック数: {len([b for b in response.content if b.type == 'tool_use'])}\n")

if response.stop_reason == "tool_use":
    my_messages.append({"role": "assistant", "content": response.content})
    
    my_tool_results = []

    # ① response.content の全ブロックを表示（text / tool_use が混在することがある）
    print("--- response.content の構造 ---")
    for i, block in enumerate(response.content):
        if block.type == "tool_use":
            print(f"  [{i}] tool_use  name={block.name}  id={block.id}  input={block.input}")
        else:
            print(f"  [{i}] text      '{block.text[:30]}...'")
    print()

    for block in response.content:
        if block.type == "tool_use":
            print(f"  ツール呼び出し: {block.name}({block.input})")
            my_result = run_tool(block.name, block.input)
            # ② ツールの実行結果を表示
            print(f"    → 実行結果: {my_result}")
            my_tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": my_result
            })

    # ③ Claudeに返す tool_results の構造を表示
    print("\n--- Claudeに返す tool_results ---")
    for r in my_tool_results:
        print(f"  tool_use_id={r['tool_use_id']}")
        print(f"  content    ={r['content']}")

    my_messages.append({"role": "user", "content": my_tool_results})
    
    my_final = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 1024,
        tools = my_tools,
        messages = my_messages
    )

print(f"\nClaude の最終回答:\n{my_final.content[0].text}")

print("\n\n=== パート2: tool_choice の比較 ===\n")

MY_QUESTION = "こんにちは！" 

for my_choice in [
    {"type": "auto"},
    {"type": "any"},
    {"type": "tool", "name" : "get_current_datetime"},
    ]:
    
    response = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 256,
        tools = my_tools,
        tool_choice = my_choice,
        messages = [{"role": "user", "content": MY_QUESTION}]
    )
    print(f"tool_choice={my_choice['type']:4s}  stop_reason={response.stop_reason}")

    # ④ ツールが呼ばれた場合、ループを完成させて最終回答を確認する
    if response.stop_reason == "tool_use":
        called = [b.name for b in response.content if b.type == "tool_use"]
        print(f"           → 呼ばれたツール: {called}")

        # ツール結果を組み立てて返す（パート1と同じ流れ）
        my_p2_messages = [{"role": "user", "content": MY_QUESTION}]
        my_p2_messages.append({"role": "assistant", "content": response.content})

        my_p2_results = []
        for block in response.content:
            if block.type == "tool_use":
                my_result = run_tool(block.name, block.input)
                my_p2_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": my_result
                })
        my_p2_messages.append({"role": "user", "content": my_p2_results})

        my_p2_final = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            tools=my_tools,
            messages=my_p2_messages
        )
        # 「こんにちは！」への返答でツール結果（日時など）が使われるか確認
        print(f"           → 最終回答: {my_p2_final.content[0].text[:80]}...")
    print()