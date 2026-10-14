# 試験シナリオ集（CCA-F Exam Guide Chapter 5）

> 試験では6シナリオから4つがランダムに出題される。各問題はいずれか1つのシナリオを前提としたシナリオベース形式。

---

## クイックリファレンス

| # | シナリオ名 | 主要ドメイン |
|---|-----------|------------|
| 1 | Customer Support Resolution Agent | Agentic Architecture, Tool/MCP, Context Management |
| 2 | Code Generation with Claude Code | Claude Code Config, Context Management |
| 3 | Multi-Agent Research System | Agentic Architecture, Tool/MCP, Context Management |
| 4 | Developer Productivity with Claude | Tool/MCP, Claude Code Config, Agentic Architecture |
| 5 | Claude Code for Continuous Integration | Claude Code Config, Prompt Engineering/Structured Output |
| 6 | Structured Data Extraction | Prompt Engineering/Structured Output, Context Management |

---

## Scenario 1: Customer Support Resolution Agent

**背景:**
Claude Agent SDK を使ってカスタマーサポートの解決エージェントを構築している。
返品、請求トラブル、アカウント問題など曖昧度の高いリクエストを処理する。

**利用可能なMCPツール:**
- `get_customer` — 顧客情報の取得
- `lookup_order` — 注文の照会
- `process_refund` — 返金処理
- `escalate_to_human` — 人間へのエスカレーション

**目標:** ファーストコンタクト解決率 80%以上を維持しつつ、適切なエスカレーション判断を行う。

**主要ドメイン:**
- `Agentic Architecture & Orchestration`
- `Tool Design & MCP Integration`
- `Context Management & Reliability`

---

## Scenario 2: Code Generation with Claude Code

**背景:**
Claude Code を使ってソフトウェア開発を加速している。
コード生成、リファクタリング、デバッグ、ドキュメント作成に活用している。

**課題:**
- カスタムスラッシュコマンドの整備
- `CLAUDE.md` の設定
- Plan mode vs Direct execution の使い分け判断

**主要ドメイン:**
- `Claude Code Configuration & Workflows`
- `Context Management & Reliability`

---

## Scenario 3: Multi-Agent Research System

**背景:**
Claude Agent SDK を使ってマルチエージェントリサーチシステムを構築している。
コーディネーターエージェントが専門サブエージェントに委任する構成。

**サブエージェント構成:**
| エージェント | 役割 |
|------------|------|
| Web Search Agent | Web検索 |
| Document Analysis Agent | ドキュメント分析 |
| Synthesis Agent | 調査結果の統合 |
| Report Agent | レポート生成 |

**出力:** トピックに関する包括的な引用付きレポート

**主要ドメイン:**
- `Agentic Architecture & Orchestration`
- `Tool Design & MCP Integration`
- `Context Management & Reliability`

---

## Scenario 4: Developer Productivity with Claude

**背景:**
Claude Agent SDK を使って開発者生産性ツールを構築している。
エンジニアが不慣れなコードベースを探索・理解し、定型コードを生成・自動化するのを支援する。

**利用可能なビルトインツール:**
- `Read` / `Write` / `Bash` / `Grep` / `Glob`
- MCPサーバーとの統合

**主要ドメイン:**
- `Tool Design & MCP Integration`
- `Claude Code Configuration & Workflows`
- `Agentic Architecture & Orchestration`

---

## Scenario 5: Claude Code for Continuous Integration

**背景:**
Claude Code を CI/CDパイプラインに統合している。
自動コードレビュー、テストケース生成、プルリクエストへのフィードバック提供を行うシステム。

**課題:**
- 実行可能なフィードバックを生成するプロンプト設計
- 誤検知（False Positive）の最小化

**主要ドメイン:**
- `Claude Code Configuration & Workflows`
- `Prompt Engineering & Structured Output`

---

## Scenario 6: Structured Data Extraction

**背景:**
Claude を使って構造化データ抽出システムを構築している。
非構造化ドキュメントから情報を抽出し、JSONスキーマで検証、ダウンストリームシステムと統合する。

**要件:**
- エッジケースの適切な処理
- 高精度の維持
- ダウンストリームシステムとの統合

**主要ドメイン:**
- `Prompt Engineering & Structured Output`
- `Context Management & Reliability`
