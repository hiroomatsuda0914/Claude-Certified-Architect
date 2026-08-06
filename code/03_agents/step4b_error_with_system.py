import anthropic
import file_tool

client = anthropic.Anthropic()
my_tools = [file_tool.definition]

my_system = """あなたはファイル読み込みアシスタントです。

## エラー時のルール
- ファイルが見つからない場合は、以下の順で代替ファイルを1回だけ試してください
  1. ファイル名の先頭に「data_」を付けて再試行（例: report.txt → data_report.txt）
  2. それでも見つからない場合は、ユーザーにファイルが存在しないことを伝えて終了する
- 権限エラーの場合は、リトライせずにすぐユーザーに報告する
"""

def run_agent(question):
    my_messages = [{"role": "user", "content": question}]
    iteration = 0
    MAX_ITERATIONS = 2
    
    
    while True:
        print(f"\n--- ループ開始 ---")
        
        iteration += 1
        if iteration > MAX_ITERATIONS:
            my_messages.append({"role" : "user", "content": "処理の上限に達しました。ここまでの結果をユーザーに報告してください。"})
            
            final = client.messages.create(
                model = "claude-haiku-4-5",
                max_tokens = 300,
                tools = my_tools,
                messages = my_messages,
                system = my_system
            )
            print(f" [エラー] 最大反復回数 {MAX_ITERATIONS} に達しました。終了します。")
            print(f" [上限到達] {final.content}")
            break

        response = client.messages.create(
            model = "claude-haiku-4-5",
            max_tokens = 300,
            tools = my_tools,
            messages = my_messages,
            system = my_system
        )
        
        print(f" [Claudeの応答] stop_reason: {response.stop_reason}, content: {response.content}")
        
        if response.stop_reason == "tool_use":
            tool_block = next (b for b in response.content if b.type == "tool_use")
            print(f" [ツール呼び出し]{tool_block.name}({tool_block.input})")
            
            my_result = file_tool.run_good(tool_block.input["filename"])
            print(f" [ツールの戻り値] '{my_result}'")
            
            my_messages.append({"role" : "assistant", "content": response.content})
            my_messages.append({"role" : "user", "content":[
                {
                    "type" : "tool_result",
                    "tool_use_id" : tool_block.id,
                    "content" : my_result
                }
            ]})
            
        elif response.stop_reason == "end_turn":
            print(f" [Claudeの最終的な応答] '{response.content[0].text}'")
            break
    
        else:
            print(f" [Claudeの最終的な応答] '{response.content[0].text}'")
            break

print("=" * 50)
print("report.txt を読んでください（存在しないファイル）")
print("=" * 50)
run_agent("report.txt の内容を教えてください")