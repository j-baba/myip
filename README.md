# myip
固定IPを持たないサーバが自分のプライベートIP(wlan0)をGMAILに通知するスクリプト。

元々、ラズパイあたりを想定したもので、Wi-Fiで取得したIPを知る前提で作っているので、IPを取得するインターフェイスがwlan0ベタ書きになってます。

## 導入手順
gitからプログラムのダウンロード
```
git clone git@github.com:j-baba/myip.git
cd myip
```

venv仮想環境作成
※この辺は導入環境に合わせてください。
```
python3 -m venv venv
source venv/bin/activate
```

必要なPythonパッケージのインストール
```
pip install -r requirements.txt
```

設定ファイルの手動作成
※この記載はGmail用です。必要に応じて修正を。
※Gmailを使用する場合、パスワードはGoogleアプリパスワードにしないと認証エラーが出ました。
　下記URLから登録し、表示される16桁のパスワードを登録してください。
　https://myaccount.google.com/apppasswords
```
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "xxxxxx@gmail.com" # 送信元メールアドレス
GMAIL_PASSWORD = "xxxxxxxxxxxxxxxx" # Googleアプリパスワード
TO_EMAIL = "xxxxxx@gmail.com" # 送信先メールアドレス
IP_FILE = "/path/to/file/myip.txt" # IPアドレスを保存するファイル
```

## 実行
手動実行
```
/path/to/file/venv/bin/python /path/to/file/myip.py
```

定期実行
```
crontab -e
```
```
*/5 * * * * cd /path/to/file; venv/bin/python myip.py > /tmp/cron.log 2>&1
```
