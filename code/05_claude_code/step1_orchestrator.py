import anthropic
import specialist

client = anthropic.Anthropic()

# ─────────────────────────────────────────
# オーケストレーターのツール定義
# specialist.definition を渡す（Phase 2 の weather_tool.definition と同じ）
# ─────────────────────────────────────────

my_tools = [specialist.definition]

my_system = "あなたはオーケストレーターです。ユーザーの質問を適切な専門分野に振り分け、ask_specialist ツールで回答を得てください。"

def run_orchestrator(user_question: str) -> str:
    my_messages = [{"role": "user", "content": user_question}]
    
    while True:
        response = client.messages.create(
            model = "claude-haiku-4-5-20251001",
            max_tokens=500,
            system=my_system,
            tools=my_tools,
            messages=my_messages,
        )
        
        print(f"  [stop_reason] {response.stop_reason}")
        
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
                
        if response.stop_reason == "tool_use":
            my_messages.append({"role": "assistant", "content": response.content})
            
            my_tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [blockの中身]{block}")
                    print(f"  [orchectrator] specialty = {block.input['specialty']}")
                    
                    my_answer = specialist.run(
                        block.input["specialty"],
                        block.input["question"]
                    )
                    print(f"  [subagent]     {my_answer[:60]}...")
                    
                    my_tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": my_answer,
                    })
            
            my_messages.append({"role": "user", "content": my_tool_results})
            
            
# 実行

if __name__ == "__main__":
    my_questions = [
        "アジアで一番高い山は？",
        "世界一大きい魚は？",
    ]
    
    for q in my_questions:
        print(f"\n質問: {q}")
        print("="*50)
        my_result = run_orchestrator(q)
        print(f"最終回答：{my_result}")