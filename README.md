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

## Local development

Python 3.12以上を用意し、仮想環境で依存関係をインストールします。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

アプリを起動します。

```bash
uvicorn app.main:app --reload
```

起動後、<http://127.0.0.1:8000/> にアクセスするとHTTP 200と `{"status":"ok"}` が返ります。

テストを実行します。

```bash
pytest -q
```

現在のIssue #2では、アプリ基盤とルートエンドポイントの疎通確認までを扱います。システム情報APIとDashboard UIは後続Issueで実装します。
