import os

definition = {
    "name": "read_file",
    "description": "指定したファイルの内容を読み込む",
    "input_schema": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "読み込むファイルの名前"
            }
        },
        "required": ["filename"]
    }
}


def run_bad(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def run_good(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"エラー: ファイル '{filename}' が見つかりません。別のファイル名を試してください。"