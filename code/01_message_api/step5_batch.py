import anthropic
import time
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


client = anthropic.Anthropic()

# === パート1: バッチ作成 ===
print("=== パート1: バッチ作成 ===")

my_request = [
    Request(
        custom_id="q1",
        params=MessageCreateParamsNonStreaming(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "What is the capital of France?"}
            ]
        )
    ),
    Request(
        custom_id="q2",
        params=MessageCreateParamsNonStreaming(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "What is the capital of China?"}
            ]
        )
    ),
    Request(
        custom_id="q3",
        params=MessageCreateParamsNonStreaming(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "What is the capital of Germany?"}
            ]
        )
    ), 
]

my_batch = client.messages.batches.create(requests = my_request)
print(f"Batch ID        : {my_batch.id}")
print(f"Status          : {my_batch.processing_status}")
print(f"リクエスト件数  : {my_batch.request_counts.processing}件処理中\n")


# === パート2: 完了待ち（ポーリング）===
print("=== パート2: 完了待ち ===")

while True:
    my_batch = client.messages.batches.retrieve(my_batch.id)
    if my_batch.processing_status == "ended":
        break
    print(f"処理中... {my_batch.request_counts.processing}件残り")
    time.sleep(5)
    
print(f"完了！ succeeded={my_batch.request_counts.succeeded} / " f"errored={my_batch.request_counts.errored}\n")

# === パート3: 結果取得 ===
print("=== パート3: 結果取得 ===")

for result in client.messages.batches.results(my_batch.id):
    if result.result.type == "succeeded":
        my_text = result.result.message.content[0].text
        print(f"[{result.custom_id}] 成功: {my_text}")
    else:
        print(f"[{result.custom_id}] 失敗: {result.result.error}")
