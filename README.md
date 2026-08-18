# system-monitor-dashboard

ローカルPCの状態をブラウザから確認する小規模なシステムモニターダッシュボードです。
Nine標準AI開発フローの実証用プロジェクトとして、Issueを仕様の基準にしています。

## V1の対象

- CPU使用率
- メモリ使用量
- ディスク使用量
- OS情報
- Uptime
- `GET /api/system`
- Webダッシュボード
- 5秒間隔の自動更新
- API取得失敗時のエラー表示と復旧

## V1で対応しないもの

GPU、温度、ネットワーク、Docker、ローカルLLM、履歴保存、認証、通知、グラフ表示は対象外です。

## 技術構成

- Python 3.12以上
- FastAPI / Uvicorn
- psutil
- HTML / CSS / JavaScript
- pytest
- GitHub Actions

## セットアップ

仮想環境を作成し、依存関係をインストールします。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 起動

プロジェクトルートで次を実行します。

```bash
uvicorn app.main:app --reload
```

ブラウザで <http://127.0.0.1:8000/> を開くとDashboardが表示されます。
CPU、Memory、Disk、OS、Uptime、Last Updateが表示され、5秒ごとに最新値へ更新されます。

APIが一時的に利用できない場合はエラー表示になり、APIが復旧すると自動的にLive表示へ戻ります。

## 主要API

### `GET /`

ブラウザのHTMLリクエストにはDashboardを返します。
JSONクライアントなどHTMLを要求しないリクエストには、互換性維持のため次を返します。

```json
{"status": "ok"}
```

### `GET /api/system`

現在のシステム情報をJSONで返します。

```json
{
  "cpu_percent": 24.1,
  "memory": {"used_gb": 8.5, "total_gb": 16.0, "percent": 53.1},
  "disk": {"used_gb": 143.0, "total_gb": 256.0, "percent": 55.9},
  "os": "macOS",
  "uptime_seconds": 301400
}
```

CPU、Memory、Diskの割合は0から100までのパーセント値です。
メモリとディスクの容量はGB、Uptimeは秒で返します。

## テスト

通常のテストとPythonのimport / syntaxチェックを実行します。

```bash
pytest -q
python -m compileall -q app tests
```

統合テストでは、HTMLとしてのトップページ、静的ファイル、`/api/system`の到達性とレスポンスを確認します。

## 手動確認

1. READMEの手順でアプリを起動する。
2. ブラウザでDashboardを開き、5つのメトリクスとLast Updateを確認する。
3. 5秒以上待ち、Last Updateと値が更新されることを確認する。
4. Uvicornを停止し、エラー表示とUpdate failed表示を確認する。
5. Uvicornを再起動し、Live表示へ戻ることを確認する。

## 開発ルール

GitHub Issueを仕様の基準とし、原則 **1子Issue = 1 PR** で進めます。
詳細なルールは `AGENTS.md` を参照してください。
