
# ─────────────────────────────────────────
# ツール定義（Claudeに渡すJSONスキーマ）
# Claudeはこれを読んで「使えるツール」を把握する
# ─────────────────────────────────────────
definition = {                          # {} = 辞書。ツール1つ分の定義をキーと値で表現
    "name": "get_weather",              # Claudeがツールを識別する名前
    "description": "指定した都市の天気を返す",  # Claudeがこれを読んで使うか判断する
    "input_schema":{
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "都市名（例：Tokyo）"
            }
        },
        "required": ["city"]            # Claudeが必ず city を渡してくることを保証する
    }
}

# ─────────────────────────────────────────
# ツール実装（ローカルで実行する関数）
# Claudeはこの関数の存在を知らない。呼ぶのは自分のコード
# ─────────────────────────────────────────
def run(city):                          # city はClaudeが決めた引数（step2b_main.pyで渡す）
    my_data = {                         # {} = 辞書。都市名（キー）→ 天気（値）のマッピング
        "Tokyo": "晴れ",
        "Osaka": "曇り",
        "Kyoto": "雨"
    }
    return my_data.get(city, "天気が不明です")  # 戻り値はClaudeに返すための文字列