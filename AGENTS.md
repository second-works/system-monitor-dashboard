# AGENTS.md

## Purpose

このプロジェクトはNine標準AI開発フローの実証用 `system-monitor-dashboard` です。

GitHub Issueを実装仕様の基準とし、CodexはIssue単位で作業します。

## Core Rules

- 原則として **1子Issue = 1 PR**。
- Issue範囲外を実装しない。
- 依存Issueが未完了なら原則着手しない。
- 不要なリファクタリングをしない。
- 既存動作を壊さない。
- 新規機能・バグ修正には必要なテストを追加する。
- `main`へ直接pushしない。
- force pushしない。
- `.env`、API key、token、password等の秘密情報をcommitしない。
- 仕様が不明確な場合は推測で拡張しない。
- 実装後はローカルテストを行い、PR作成後はGitHub Actions CI結果も確認する。

## V1 Scope

実装対象:

- CPU使用率
- メモリ使用量
- ディスク使用量
- OS情報
- Uptime
- `GET /api/system`
- Web UI
- 自動更新
- エラー表示

V1で実装しないもの:

- GPU監視
- 温度監視
- ネットワーク監視
- Docker監視
- ローカルLLM監視
- データベース / 履歴保存
- 認証
- 通知
- グラフ表示

## Project Structure

想定構成:

```text
app/
  main.py
  system_info.py
  static/
    app.js
    style.css
  templates/
    index.html
tests/
  test_api.py
  test_system_info.py
```

## Validation

プロジェクトで定義後、PR前に可能な範囲で以下を実行する。

- `pytest`
- lint
- import / syntax check

GitHub Actions CIが失敗しているPRは完了扱いにしない。

## Pull Requests

PR本文には最低限以下を書く。

- `Closes #<Issue番号>`
- 変更内容
- ローカルテスト結果
- GitHub Actions CI結果
- 注意点 / 残課題

## Human Decision Points

以下は人間の判断を優先する。

- 仕様変更
- Issue範囲変更
- 破壊的変更
- セキュリティ上重要な判断
- CI例外
- `main`へのmerge
