# Cursor 学習進捗

正答率は試験の5ドメインだけ記録する。個別の TEST OBJECTIVE の全文、問題文、選択肢、解説は残さない。

未解答は不正解として数える。正答率は正解数 ÷ 出題数。出題が 0 の正答率は「—」。

最終更新: 2026-11-09  
練習合計: 出題 166 / 正解 135 / 正答率 81%

## ドメイン別の正答率

| ドメイン | 出題 | 正解 | 正答率 |
|----------|------|------|--------|
| Agentic Architecture & Orchestration | 42 | 34 | 81% |
| Tool Design & MCP Integration | 24 | 21 | 88% |
| Claude Code Configuration & Workflows | 31 | 26 | 84% |
| Prompt Engineering & Structured Output | 33 | 26 | 79% |
| Context Management & Reliability | 38 | 30 | 79% |
| **合計** | **166** | **135** | **81%** |

## 誤答メモ

間違えた観点だけを残す。その観点で後から正答したら、その行は削除する。

### Agentic Architecture & Orchestration

### Tool Design & MCP Integration

### Claude Code Configuration & Workflows

### Context Management & Reliability

### Prompt Engineering & Structured Output
- false positive削減には後続パスによる上書きでなく、除外条件・許容パターンをプロンプトに明示することが必要

## シナリオ別出題数

| シナリオ | 出題数 |
|---------|--------|
| Scenario 1: Customer Support Resolution Agent | 25 |
| Scenario 2: Code Generation with Claude Code | 26 |
| Scenario 3: Multi-Agent Research System | 26 |
| Scenario 4: Developer Productivity with Claude | 26 |
| Scenario 5: Claude Code for Continuous Integration | 25 |
| Scenario 6: Structured Data Extraction | 25 |


## Test Objectivesカバレッジ

→ [`test_objectives.md`](./test_objectives.md) を参照・更新すること。

## 出題スキップ（習得済み）

十分に理解済みのため、同趣旨の問題は出さない。

- tool_choice + JSON schema によるスキーマ準拠の強制（structured output enforcement）
- nullable / optional フィールドによる欠損値の表現（捏造を防ぐスキーマ設計）
- 高リスクな変更では plan mode で承認まで編集を止め、承認後に同じセッションで計画を適用する（ファイル単位の許可や、編集後の要約では代替しない）
