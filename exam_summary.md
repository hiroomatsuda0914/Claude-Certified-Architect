# Claude Certified Architect Foundations — 受験記録

## 受験結果

| 受験 | 日付 | スコア | 合格ライン | 結果 |
|------|------|--------|------------|------|
| 第1回 | 2026-10-12 | 603 | 720 | Fail |
| 第2回 | 2026-11-13 | 742 | 720 | **Pass** |

---

## 合格までの流れ

### 第1回受験前

- Claude API・Claude Code の各機能をハンズオンで実装しながら学習（Phase 1〜8）
  - Messages API、Tool Use、Agents、MCP、Claude Code、エンタープライズ統合、Webアプリ、セキュリティ
- Gemini を使って200問以上の練習問題を解き、正答率90%超を記録
- 学習完了の手応えで受験したが、**603点で不合格**（合格ライン720）

### 第1回の振り返りと再対策

第1回の結果から、0%項目が12個あることが判明。練習問題の形式と本番シナリオ形式の乖離が主因と分析し、以下の方針で再対策を実施：

- **学習方針の転換**：点数の暗記から「なぜその選択か」の判断軸の習得へ
- **Claude Code での練習問題**：本番に近い四択シナリオ形式で出題
  - 問題文に前提・シナリオを明示
  - 誤答はすべて「一見正しそうな選択肢」に設定（難易度本番相当）
  - 解説は日本語、問題文・選択肢は英語
- **弱点項目に集中**：0%だった12項目を最優先でカバー
- **練習合計**：244問 / 正答率82%（2026-11-12時点）

### 第2回受験

- 英語受験で再挑戦（2026-11-13）
- **742点で合格**（+139点）

---

## 第2回スコアレポート詳細

### 100%（完全習得）

| Test Objective |
|----------------|
| Design structured handoff packages |
| Decompose complex tasks into dynamically generated subtasks |
| Apply PreToolUse and PostToolUse hook patterns |
| Create and deploy custom slash commands |
| Determine when to use plan mode versus direct execution |
| Distinguish settings/hooks instructions from CLAUDE.md |
| Select the correct Claude Code configuration mechanism |
| Implement PostToolUse hooks for code quality constraints |
| Apply systematic codebase exploration strategies |
| Select the appropriate method for providing project context |
| Explain why conversation history must be explicitly included in each API request |
| Select the appropriate API processing mode |
| Select and implement the most reliable structured output method |
| Implement tool use with defined JSON schemas |
| Design feedback loop mechanisms |
| Implement MCP tool error handling |
| Integrate MCP servers into Claude Code and agent applications |
| Configure the tool_choice parameter |

### 50〜83%（部分正解）

| Test Objective | スコア |
|----------------|--------|
| Apply session resumption techniques | 83% |
| Apply extraction accuracy patterns | 75% |
| Design extraction schemas with optional fields | 67% |
| Design human review routing strategies | 33% |
| Explain how the agentic loop uses stop_reason signals | 50% |
| Structure iterative refinement workflows | 50% |
| Improve tool selection reliability by expanding tool descriptions | 50% |

### 0%（未習得）

| Test Objective | 備考 |
|----------------|------|
| Design orchestration-layer safeguards (agentic loopの終了保証) | 新出題 |
| Configure MCP servers and project settings at the correct scope | 新出題 |
| Apply context management strategies (長期セッション) | 前回100%から後退 |
| Apply escalation decision criteria | 新出題 |

---

## 第1回 → 第2回 の変化

### 大幅改善（前回0% → 今回100%）

| 項目 |
|------|
| Decompose complex tasks（動的タスク分解） |
| Select the correct Claude Code configuration mechanism（設定機構選択） |
| Select and implement the most reliable structured output method |
| Configure the tool_choice parameter |

### その他の改善

| 項目 | 第1回 | 第2回 |
|------|-------|-------|
| Integrate MCP servers | 50% | 100% |
| Apply systematic codebase exploration | 80% | 100% |

### 後退した項目

| 項目 | 第1回 | 第2回 |
|------|-------|-------|
| Apply context management strategies | 100% | 0% |
| Structure iterative refinement workflows | 100% | 50% |
| Apply extraction accuracy patterns | 100% | 75% |

### 固定的弱点（2回連続で低スコア）

| 項目 | 第1回 | 第2回 |
|------|-------|-------|
| Design human review routing strategies | 33% | 33% |

---

## 今回0%項目のポイント（次回受験・レベルアップのための記録）

### Orchestration-layer safeguards（agentic loopの終了保証）
- agentic loopがどう終了しても（正常完了・エラー・タイムアウト）、必ず「解決済み」か「人間エスカレーション」で終わる設計
- stop_reasonやエラー状態に応じた終了分岐を明示的に設計する

### Configure MCP servers scope（project vs user）
- **project-level**：チームで共有するツール（リポジトリの`.claude/`に置く）
- **user-level**：個人の実験的・一時的な設定（`~/.claude/`に置く）
- 判断軸：「チームが使うか、自分だけか」

### Apply context management strategies（長期セッション）
- 対策手段：サブエージェント分離・スクラッチパッドファイル・必要ファイルの絞り込み読み込み
- セッションをまたぐ場合は状態をファイルに書き出して保存

### Escalation decision criteria（エスカレーション判断基準）
- ユーザーが「人間に繋いでほしい」と明示したら**即座に従う**（自律解決を試みない）
- ツール失敗のみではエスカレーション条件にならない
- 判断軸：「権限外・高リスク・ユーザー明示 → 即エスカレーション」「ツール失敗のみ → 自律継続」

### Design human review routing strategies（固定的弱点）
- **ランダムサンプリングは不正解**
- confidence scoreが低い抽出、非定型フォーマット、フィールド単位の曖昧さ でルーティングを決める
- 文書全体ではなく、曖昧なフィールドにフラグを立てる
