# Cursor 学習進捗

正答率は試験の5ドメインだけ記録する。個別の TEST OBJECTIVE の全文、問題文、選択肢、解説は残さない。

未解答は不正解として数える。正答率は正解数 ÷ 出題数。出題が 0 の正答率は「—」。

最終更新: 2026-11-12  
練習合計: 出題 244 / 正解 199 / 正答率 82%

## ドメイン別の正答率

| ドメイン | 出題 | 正解 | 正答率 |
|----------|------|------|--------|
| Agentic Architecture & Orchestration | 65 | 51 | 78% |
| Tool Design & MCP Integration | 29 | 25 | 86% |
| Claude Code Configuration & Workflows | 41 | 35 | 85% |
| Prompt Engineering & Structured Output | 53 | 43 | 81% |
| Context Management & Reliability | 56 | 45 | 80% |
| **合計** | **244** | **199** | **82%** |

## 誤答メモ

間違えた観点だけを残す。その観点で後から正答したら、その行は削除する。

### Agentic Architecture & Orchestration
### Tool Design & MCP Integration
### Claude Code Configuration & Workflows
### Context Management & Reliability

### Prompt Engineering & Structured Output

## シナリオ別出題数

| シナリオ | 出題数 |
|---------|--------|
| Scenario 1: Customer Support Resolution Agent | 38 |
| Scenario 2: Code Generation with Claude Code | 38 |
| Scenario 3: Multi-Agent Research System | 39 |
| Scenario 4: Developer Productivity with Claude | 38 |
| Scenario 5: Claude Code for Continuous Integration | 38 |
| Scenario 6: Structured Data Extraction | 38 |


## Test Objectivesカバレッジ

→ [`test_objectives.md`](./test_objectives.md) を参照・更新すること。

## 出題スキップ（習得済み）

十分に理解済みのため、同趣旨の問題は出さない。

- tool_choice + JSON schema によるスキーマ準拠の強制（structured output enforcement）
- nullable / optional フィールドによる欠損値の表現（捏造を防ぐスキーマ設計）
- 高リスクな変更では plan mode で承認まで編集を止め、承認後に同じセッションで計画を適用する（ファイル単位の許可や、編集後の要約では代替しない）
- scratchpadファイルに発見内容を書き出して次のセッションで読み込む（セッション間のコンテキスト継続・コードベース探索の再開）
- プリフィル（アシスタントターンの先頭に部分テキストを埋め込み出力先頭を物理的に制御する手法）
- ツールの誤選択・ミスルーティングの改善策（ツール説明文の改善、名前変更、統合、chain-of-thought追加など）の中から最適な手法を選ぶ問題
- MCPサーバーの設定ファイル配置場所（プロジェクトレベルは .claude/settings.json、グローバルは ~/.claude/settings.json、CLAUDE.mdには書かない）
- CIレビューの false positive 削減は、プロジェクト固有の慣習・許容パターン・除外基準をシステムプロンプトに永続コンテキストとして注入し、生成段階で抑える
- plan mode はタスクのリスクレベルと影響範囲（下流への波及）で選択する。ファイル数・タスク数などの量的閾値は判断基準にならない
- 安定した参照データは MCP resource としてホストが読み込み、副作用のある操作（返金など）は tool として残す（モデルが呼ぶツールの一覧から参照データを外す）
- サブエージェントへのツール配布はプロンプト指示（ソフト制約）ではなく、設定レベルで役割に必要なツールのみを割り当てる（ハード制約）
- CI で Claude Code を非対話実行するときは、`-p` と権限モード（許可されていない操作は確認なしに拒否する設定）、`--allowedTools`、ターン数と予算の上限を組み合わせて暴走と書き込みを防ぐ
- 出典が対立する主張は、争点を両側の出典付きで明示ラベルし、合意している主張と分けて転送する（捨てる、片方を採用する、報告を待つ、は不可）
