# Claude Certified Architect — 学習プロジェクト設定

## 試験シナリオ

練習問題を出す際は **必ず `Scenarios.md` のいずれかのシナリオを前提として問題を作成すること**。
シナリオは編集せず、そのまま使用すること。
シナリオの詳細は [`Scenarios.md`](./Scenarios.md) を利用する。
シナリオと問題と解答は英語、解説の依頼があった場合は日本語とする。
練習問題の選択肢は、消去法で正解が選べないように紛らわしいものとすること。

## 練習問題の出し方

ユーザーは Claude の資格試験の勉強中である。「始めてください」、または練習問題を求められたら、次の手順で1問出す。

1. そのセッションの1問目を出す前だけ、[`Scenarios.md`](./Scenarios.md) と [`cursor_study_progress.md`](./cursor_study_progress.md) を読む。[`test_objectives.md`](./test_objectives.md) はセッション開始時には読まない。2問目以降はどのファイルも読み直さない。
2. 出題ドメインは、ランダムとする。個別の TEST OBJECTIVE は、そのドメインの中でどの観点を問うかの参考にとどめる。
3. TEST OBJECTIVE の一覧、`scorereport.pdf`、試験ガイド、`練習問題_進捗.md` は読まない。チャットに TEST OBJECTIVE の英文を書き出さない。
4. `cursor_study_progress.md` の「シナリオ別出題数」を参照し、出題数が最も少ないシナリオを優先して選ぶ。同数の場合はランダム。選んだシナリオを前提にした、本番レベルの四択を1問出す。
5. シナリオ、問題、選択肢、解答は英語で書く。解説は、ユーザーが依頼した場合だけ日本語で書く。解説は短くする。
6. 解答はユーザーが答えるまで出さない。「分からない」と言った場合は、その時点で正解と解説を出す。
7. 出題と解説のチャット本文に、進捗ファイル、`Scenarios.md`、過去の問題文を再掲しない。

依頼の原文:

> Claudeの資格試験の勉強中です。"C:\Users\matsuda.hiro\Desktop\Claude Certified Architect\Scenarios.md"を参照して、練習問題を出してほしいです。難易度は本番レベルで、四択でお願いします。

## 学習進捗の更新

学習進捗は [`cursor_study_progress.md`](./cursor_study_progress.md) に記録する。全問の履歴は残さない。

ユーザーが1問答えるたび、または「分からない」と答えたたびに、次の問題を出す前にこのファイルを更新する。

1. 使用したシナリオの出題数を「シナリオ別出題数」で1増やす。
2. その問題を、次の5ドメインの1つだけに対応づける。
   - Agentic Architecture & Orchestration
   - Tool Design & MCP Integration
   - Claude Code Configuration & Workflows
   - Prompt Engineering & Structured Output
   - Context Management & Reliability
   - 合計も更新する
3. 対応する行の出題数を1増やす。正解なら正解数も1増やす。正答率は正解数 ÷ 出題数とする。未解答は不正解として数える。練習合計も更新する。更新は該当行と、必要な誤答メモだけを置換する。
4. 不正解または未解答のときだけ、そのドメインの誤答メモに、間違った観点を1行追加する。同じ観点のメモが既にあれば追加しない。正解のときはメモを追加しない。
5. 同じ観点で後から正答したら、その誤答メモは削除する。
6. 正誤に限らず出題したら、[`test_objectives.md`](./test_objectives.md) を読み、該当する目標を「未出題」→「出題済」に移動する。全て出題済になったら周回数を1増やして全項目を「未出題」に戻す。
7. 問題文、選択肢、解説、日付、シナリオ名、TEST OBJECTIVE の全文は記録しない。ファイル全体をチャットに再掲しない。
8. CursorとClaudeで並行して編集しているので、出題数や正答率の更新時には、単純にその時点のファイルの状態から更新をすれば良い。（更新前の状態との比較は不要）。

セッションをリセットしても、`cursor_study_progress.md` と `Scenarios.md` を読めば学習を継続できること。
