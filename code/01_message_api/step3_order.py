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


def ask_wrong_order(user_name, question):
    """❌ 動的コンテンツが先：キャッシュが効かない"""
    my_system = [
        {
            "type": "text",
            "text": f"対応ユーザー: {user_name}"       # 動的が先
        },
        {
            "type": "text",
            "text": MY_MANUAL,
            "cache_control": {"type": "ephemeral"}     # 静的が後
        }
    ]
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        system=my_system,
        messages=[{"role": "user", "content": question}]
    )
    usage = response.usage
    print(f"  cache_creation: {usage.cache_creation_input_tokens}")
    print(f"  cache_read    : {usage.cache_read_input_tokens}")


def ask_correct_order(user_name, question):
    """✅ 静的コンテンツが先：キャッシュが効く"""
    my_system = [
        {
            "type": "text",
            "text": MY_MANUAL,
            "cache_control": {"type": "ephemeral"}     # 静的が先
        },
        {
            "type": "text",
            "text": f"対応ユーザー: {user_name}"       # 動的が後
        }
    ]
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        system=my_system,
        messages=[{"role": "user", "content": question}]
    )
    usage = response.usage
    print(f"  cache_creation: {usage.cache_creation_input_tokens}")
    print(f"  cache_read    : {usage.cache_read_input_tokens}")


print("=== ❌ 間違った順序 ===")
print("1回目:")
ask_wrong_order("田中さん", "返品ポリシーを教えてください")
print("2回目（ユーザーが変わった）:")
ask_wrong_order("鈴木さん", "保証期間はどのくらいですか？")

print("\n=== ✅ 正しい順序 ===")
print("1回目:")
ask_correct_order("田中さん", "返品ポリシーを教えてください")
print("2回目（ユーザーが変わった）:")
ask_correct_order("鈴木さん", "保証期間はどのくらいですか？")