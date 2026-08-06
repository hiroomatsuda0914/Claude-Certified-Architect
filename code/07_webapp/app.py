import anthropic
from flask import Flask, request, jsonify, render_template
from my_tools import my_tools, my_mcp_tools, run_tool

app = Flask(__name__)
client = anthropic.Anthropic()
MY_MODEL = "claude-haiku-4-5-20251001"
all_tools = my_tools + my_mcp_tools

@app.route("/")
def index():
    return render_template("index.html")


def to_dict(block):
    if block.type == "text":
        return {"type": "text", "text": block.text}
    elif block.type == "tool_use":
        return {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
    return {"type": block.type}


@app.route("/chat", methods=["POST"])
def chat():
    my_user_message = request.json["message"]
    my_messages = [{"role": "user", "content": my_user_message}]
    my_tools_used = []
    my_conversation = [{"role": "user", "content": my_user_message}]
    my_raw_messages = [{"role": "user", "content": my_user_message}]

    MAX_ITERATIONS = 10
    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MY_MODEL,
            max_tokens=1024,
            tools=all_tools,
            messages=my_messages,
        )

        if response.stop_reason == "end_turn":
            my_final_text = response.content[0].text
            my_conversation.append({"role": "assistant", "content": my_final_text})
            my_raw_messages.append({
                "role": "assistant",
                "content": [to_dict(b) for b in response.content],
            })
            return jsonify({
                "response": my_final_text,
                "tools_used": my_tools_used,
                "conversation": my_conversation,
                "raw_messages": my_raw_messages,
            })

        my_raw_messages.append({
            "role": "assistant",
            "content": [to_dict(b) for b in response.content],
        })
        my_messages.append({"role": "assistant", "content": response.content})
        my_tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[ツール呼び出し]{block.name} / 引数: {block.input}")
                my_tools_used.append(f"{block.name}({block.input})")
                my_result = run_tool(block.name, block.input)
                my_conversation.append({"role": "tool", "content": f"{block.name}({block.input}) → {my_result}"})
                my_tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": my_result,
                })
        my_raw_messages.append({"role": "user", "content": my_tool_results})
        my_messages.append({"role": "user", "content": my_tool_results})

    return jsonify({"response": "エラー：最大ループ回数に達しました"})

if __name__ == "__main__":
    app.run(debug=True)
