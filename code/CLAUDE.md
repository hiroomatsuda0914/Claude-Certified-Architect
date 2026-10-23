# Claude Certified Architect — 学習プロジェクト設定

## コーディングガイド

### 変数の命名規則（学習用）
学習中はAPIレスポンスと自分で定義した変数を区別しやすくするため、
**自分で定義した変数には `my_` 接頭辞をつける**。

```python
# 自分で定義するもの
my_tools = [...]
my_messages = [...]
my_result = get_weather(...)

# APIから返ってくるもの（接頭辞なし）
response.stop_reason
response.content
tool_block.id
```
