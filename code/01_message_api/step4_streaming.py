import anthropic
import time

client = anthropic.Anthropic()

MY_QUESTION = "日本のプログラミング言語の歴史を300字程度で教えてください"

# === パート1: 通常の呼び出し（全文が揃ってから表示）===
print("=== パート1: 通常の呼び出し（全文が揃ってから表示）===")
my_start = time.time()

response = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 400,
    messages = [{"role": "user", "content": MY_QUESTION}]
)

my_elapsed = time.time() - my_start
print(response.content[0].text)
print(f"=== 経過時間: {my_elapsed:.2f}秒 ===\n\n")


# === パート2: ストリーミング呼び出し（部分的に表示）===
print("\n\n=== パート2: ストリーミング（トークンが届くたびにリアルタイム表示）===")
my_start = time.time()

with client.messages.stream(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 400,
    messages = [{"role": "user", "content": MY_QUESTION}]
) as stream:
    for my_chunk in stream.text_stream:
        print(my_chunk, end="", flush=True)
        
    my_final_message = stream.get_final_message()
    my_usage = my_final_message.usage if my_final_message else None
        
my_elapsed = time.time() - my_start

print(f"\n\n→ 最初のトークンは即座に表示、全体完了まで {my_elapsed:.1f}秒")
print(f"  input_tokens  : {my_usage.input_tokens}")
print(f"  output_tokens : {my_usage.output_tokens}")
print(f"  stop_reason   : {my_final_message.stop_reason}")