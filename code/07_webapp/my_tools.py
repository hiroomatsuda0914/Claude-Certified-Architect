from datetime import datetime 
from MCP_server.converter_server import fahrenheit_to_celsius, celsius_to_fahrenheit

my_notes = []

# ツールの例
# ツール定義
my_tools = [
    {
        "name": "get_current_datetime",
        "description": "現在の日時を返す",
        "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
        },
    },
    {
        "name": "get_weather",
        "description": "指定した都市の天気を返す",
        "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "天気を調べる都市名",
                    }
                },
            "required": ["city"],
        },
    },
        {
        "name": "save_note",
        "description": "メモをアプリのメモリに保存する",
        "input_schema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "保存するメモの内容",
                    }
                },
            "required": ["text"],
        },
    },
            {
        "name": "get_notes",
        "description": "保存されたメモを全件取得する",
        "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
        },
    },
]

my_mcp_tools = [
          {
          "name": "celsius_to_fahrenheit",
          "description": "摂氏を華氏に変換する",
          "input_schema": {
              "type": "object",
              "properties": {
                  "celsius": {
                      "type": "number",
                      "description": "変換したい摂氏の温度",
                  }
              },
              "required": ["celsius"],
          },
      },
      {
          "name": "fahrenheit_to_celsius",
          "description": "華氏を摂氏に変換する",
          "input_schema": {
              "type": "object",
              "properties": {
                  "fahrenheit": {
                      "type": "number",
                      "description": "変換したい華氏の温度",
                  }
              },
              "required": ["fahrenheit"],
          },
      },
]

# ツール実装
def get_current_datetime():
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


def get_weather(city: str):
    my_weather_data = {
        "東京": "晴れ、気温28℃",
        "大阪": "曇り、気温26℃",
        "札幌": "雨、気温18℃",
    }
    return my_weather_data.get(city, f"{city}の天気データはありません")

def save_note(text: str) -> str:
    my_notes.append(text)
    return f"メモを保存しました：「{text}」（現在{len(my_notes)}件）"

def get_notes() -> str:
    if not my_notes:
        return "保存されたメモはありません"
    return "\n".join(f"{i+1}. {note}" for i, note in enumerate(my_notes))

def run_tool(name: str, tool_input: dict) -> str:
    if name == "get_current_datetime":
        return get_current_datetime()
    elif name == "get_weather":
        return get_weather(tool_input["city"])
    elif name == "celsius_to_fahrenheit":
        return celsius_to_fahrenheit(tool_input["celsius"])
    elif name == "fahrenheit_to_celsius":
        return fahrenheit_to_celsius(tool_input["fahrenheit"])
    elif name == "save_note":
        return save_note(tool_input["text"])
    elif name == "get_notes":
        return get_notes()
 
    return f"不明なツール: {name}"
