# system-monitor-dashboard

Nine標準AI開発フローの実証用プロジェクトです。

ローカルPCのCPU、メモリ、ディスク、OS、稼働時間をWebブラウザから確認できる小規模ダッシュボードを構築します。

## V1 scope

- CPU使用率
- メモリ使用量
- ディスク使用量
- OS情報
- Uptime
- `GET /api/system`
- Webダッシュボード
- 自動更新
- エラー表示
- テスト
- GitHub Actions CI

## Out of scope for V1

GPU、温度、ネットワーク、Docker、ローカルLLM、履歴保存、認証、通知、グラフ表示はV1では実装しません。

## Stack

- Python
- FastAPI
- psutil
- HTML / CSS / JavaScript
- pytest
- GitHub Actions

## Development workflow

GitHub Issueを仕様の基準とし、原則 **1子Issue = 1 PR** で進めます。詳細は `AGENTS.md` を参照してください。
