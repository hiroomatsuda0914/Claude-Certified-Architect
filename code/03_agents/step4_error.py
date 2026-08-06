import anthropic
import file_tool

client = anthropic.Anthropic()

my_tools = [file_tool.definition]

def run_agent(question, use_good_implementation):
    my_messages = [{"role": "user", "content": question}]
    
    response = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 300,
        tools = my_tools,
        messages = my_messages
    )
    
    if response.stop_reason == "tool_use":
        tool_block = next (b for b in response.content if b.type == "tool_use")
        print(f" Claudeが要求したファイル名：{tool_block.input['filename']}")
        
        if use_good_implementation:
            my_result = file_tool.run_good(tool_block.input["filename"])
        else:
            my_result = file_tool.run_bad(tool_block.input["filename"])
            
        print(f"ツールの戻り値: '{my_result}'")
        
        my_messages.append({"role" : "assistant", "content": response.content})
        my_messages.append({"role" : "user", "content":[
            {
                "type" : "tool_result",
                "tool_use_id" : tool_block.id,
                "content" : my_result
            }
        ]})
        
        final_response = client.messages.create(
            model = "claude-haiku-4-5",
            max_tokens = 300,
            tools = my_tools,
            messages = my_messages
        )
        
        print(f"Claudeの最終的な応答: '{final_response.content[0].text}'")
        print(f"Claudeの最終的な応答: '{final_response.content}'")
        
        
print("=" * 50)
print("❌ 悪い実装（エラーを空文字で隠す）")
print("=" * 50)
run_agent("report.txt の内容を教えてください", use_good_implementation=False)

print()
print("=" * 50)
print("✅ 良い実装（エラーをClaudeに伝える）")
print("=" * 50)
run_agent("report.txt の内容を教えてください", use_good_implementation=True)