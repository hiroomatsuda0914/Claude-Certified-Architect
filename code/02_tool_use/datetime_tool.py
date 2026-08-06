from datetime import datetime


# ─────────────────────────────────────────
# ツール定義（Claudeに渡すJSONスキーマ）
# Claudeはこれを読んで「使えるツール」を把握する
# ─────────────────────────────────────────
definition = {                          # {} = 辞書。ツール1つ分の定義をキーと値で表現
    "name": "get_current_datetime",              # Claudeがツールを識別する名前
    "description": "現在の日時を返す。ユーザーが日時を尋ねた場合に使う",  # Claudeがこれを読んで使うか判断する
    "input_schema":{
        "type": "object",
        "properties": {},
        "required": []
    }
}

# ─────────────────────────────────────────
# ツール実装（ローカルで実行する関数）
# Claudeはこの関数の存在を知らない。呼ぶのは自分のコード
# ─────────────────────────────────────────
def run():                          
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")  # 戻り値はClaudeに返すための文字列