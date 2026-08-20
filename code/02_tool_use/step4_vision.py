import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

MY_IMAGE_PATH = r"C:\Users\matsuda.hiro\Desktop\Claude Certified Architect\code\02_tool_use\Image.jpg"

my_image_data = Path(MY_IMAGE_PATH).read_bytes()
my_image_b64 = base64.b64encode(my_image_data).decode("utf-8")

my_suffix = Path(MY_IMAGE_PATH).suffix.lower()
my_media_type = "image/jpeg" if my_suffix == ".jpg" else "image/png" if my_suffix == ".png" else None

print(f"画像サイズ: {len(my_image_data):,} bytes")
print(f"Image MIME type: {my_media_type}")


# パート1
print("=== パート1: 画像の説明 ===\n")


response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 512,
    messages = [
        {
        "role": "user",
        "content": [
            {
            "type": "image",
            "source":{
                "type": "base64",
                "media_type": my_media_type,
                "data": my_image_b64,
            },
            "cache_control": {"type": "ephemeral"}      
            },
            {"type": "text",
             "text": "この画像を日本語で説明してください"
            }
        ]
    }]
)

print(response.content[0].text)
print(f"\ninput_tokens : {response.usage.input_tokens}")   # 画像は多くのトークンを消費する
print(f"output_tokens: {response.usage.output_tokens}")
print(f"cache_creation : {response.usage.cache_creation_input_tokens}")
print(f"cache_read     : {response.usage.cache_read_input_tokens}")


# パート２
print("\n\n=== パート2: 画像についての追加質問 ===\n")


my_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source":{
                "type": "base64",
                "media_type": my_media_type,
                "data": my_image_b64,
                },
                "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "この画像を日本語で説明してください"
        }
    ]
    },
    {
        "role": "assistant",
        "content": response.content
    },
    {
        "role": "user",
        "content": "画像の中で最も目立つ色は何ですか？"
        
    }
    
]

my_followup = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 512,
    messages = my_messages
    )


print(my_followup.content[0].text)
print(f"\ninput_tokens : {my_followup.usage.input_tokens}")
print(f"output_tokens: {my_followup.usage.output_tokens}")
print(f"cache_creation : {my_followup.usage.cache_creation_input_tokens}")
print(f"cache_read     : {my_followup.usage.cache_read_input_tokens}")