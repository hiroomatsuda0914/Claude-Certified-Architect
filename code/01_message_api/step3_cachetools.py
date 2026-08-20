import anthropic

client = anthropic.Anthropic()

# 長いシステムプロンプト（実務では外部ファイルから読み込むことが多い）
# キャッシュが効くには claude-sonnet 系で1024トークン以上必要
MY_MANUAL = """
# カスタマーサポート ハンドブック

## 第1章 返品・返金ポリシー
購入後30日以内であれば、未使用・未開封の商品に限り返品を受け付けます。
返品送料はお客様負担となります。返金はクレジットカードへの返金となり、
処理には5〜10営業日かかります。デジタルコンテンツの返品は原則として
受け付けておりません。ただし、技術的な問題が確認された場合はこの限りではありません。

## 第2章 保証規定
全製品に対して購入日より1年間のメーカー保証を提供しています。
保証の対象は製造上の欠陥および部品の不具合です。落下・水濡れ・
不適切な使用による故障は保証対象外となります。保証期間内の修理は
無償で対応しますが、代替品の提供は在庫状況によります。

## 第3章 配送について
通常配送は注文から3〜5営業日でのお届けとなります。
速達配送（追加料金）をご選択いただいた場合は翌営業日にお届けします。
離島・山間部など一部地域は配送日数が異なります。
5,000円以上のご注文は送料無料です。それ以下の場合は一律500円の送料が発生します。

## 第4章 お支払い方法
クレジットカード（Visa・Mastercard・JCB・Amex）、銀行振込、
コンビニ払い、電子マネー（PayPay・LINE Pay）に対応しています。
分割払いはクレジットカードのみ対応しており、3回・6回・12回から選択できます。
銀行振込の場合、ご入金確認後に発送となります。

## 第5章 会員プログラム
シルバー会員（年間購入額3万円以上）：送料無料・5%ポイント還元
ゴールド会員（年間購入額10万円以上）：送料無料・10%ポイント還元・優先サポート
プラチナ会員（年間購入額30万円以上）：送料無料・15%ポイント還元・専任担当者
ポイントの有効期限は最終購入日より1年間です。

## 第6章 お問い合わせ
営業時間は平日9:00〜18:00です。土日祝日はメール対応のみとなります。
電話：0120-XXX-XXX（無料）
メール：support@example.com（24時間受付・翌営業日回答）
チャット：サイト右下のアイコンより（営業時間内のみ）
""" * 2  # 2倍にしてトークン数を確保

my_system = [
    {
        "type": "text",
        "text": MY_MANUAL,                          # 変数を参照（クォートなし）
        "cache_control": {"type": "ephemeral"}      # ← キャッシュのポイント
    }
]

my_tools = [
    {
        "name": "lookup_order",
        "description": "注文IDで注文情報を検索します。配送状況・配達予定日・追跡番号・配送業者名を返します。注文IDが存在しない場合はエラーを返します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "注文ID（例: ORD-12345）。ORD- プレフィックスが必要です。"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "check_inventory",
        "description": "商品IDで在庫状況を確認します。現在の在庫数・入荷予定日・倉庫の場所を返します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "商品ID（例: PROD-001）"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "get_return_status",
        "description": "返品リクエストIDで処理状況を確認します。受付・審査中・承認済み・完了のいずれかを返します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "return_id": {
                    "type": "string",
                    "description": "返品ID（例: RET-001）"
                }
            },
            "required": ["return_id"]
        },
        # ↓ 最後のツールに付けると、それ以前のツール定義もまとめてキャッシュされる
        "cache_control": {"type": "ephemeral"}
    }
]


def ask(question):
    my_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=my_system,
        messages=[{"role": "user", "content": question}]
    )
    usage = my_response.usage
    print(f"\nQ: {question}")
    print(f"A: {my_response.content[0].text[:120]}...")
    print(
        f"  cache_creation : {usage.cache_creation_input_tokens:>6}  # 今回キャッシュ保存したトークン数")
    print(
        f"  cache_read     : {usage.cache_read_input_tokens:>6}  # キャッシュから読んだトークン数")
    print(f"  input_tokens   : {usage.input_tokens:>6}  # 通常課金されるトークン数")


print("=== 1回目（キャッシュ作成）===")
ask("返品ポリシーを教えてください")

print("\n=== 2回目（キャッシュ読み込み）===")
ask("利用できるツールは何がありますか？")

# --- トークン数の個別確認 ---
count_system_only = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    system=my_system,
    messages=[{"role": "user", "content": "x"}]   # ダミー1トークン
)

count_with_tools = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    system=my_system,
    tools=my_tools,
    messages=[{"role": "user", "content": "x"}]   # ダミー1トークン
)

my_system_tokens = count_system_only.input_tokens - 1   # ダミーの1トークンを引く
my_tools_tokens = count_with_tools.input_tokens - count_system_only.input_tokens

print("\n=== トークン内訳 ===")
print(f"  システムプロンプト : {my_system_tokens:>6} tokens")
print(f"  ツール定義合計     : {my_tools_tokens:>6} tokens")
print(f"  合計               : {my_system_tokens + my_tools_tokens:>6} tokens")
print(f"  ※ cache_creation={my_system_tokens + my_tools_tokens} と一致するはず")
