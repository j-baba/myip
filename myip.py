import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import subprocess
import os

# 設定部分
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
GMAIL_USER = os.environ.get('GMAIL_USER')  # 送信元メールアドレス
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Gmailアプリパスワード
TO_EMAIL = os.environ.get('TO_EMAIL')  # 送信先メールアドレス
IP_FILE = os.environ.get('IP_FILE')  # IPアドレスを保存するファイル

def get_current_ip(interface="wlan0"):
    """指定されたインターフェースのIPv4アドレスを取得する"""
    try:
        # `ip`コマンドでインターフェース情報を取得
        result = subprocess.run(
            ["ip", "-4", "addr", "show", interface],
            capture_output=True,
            text=True,
            check=True
        )
        # 結果からIPアドレスを抽出
        for line in result.stdout.split("\n"):
            if "inet" in line:
                return line.strip().split()[1].split("/")[0]
    except subprocess.CalledProcessError:
        print(f"Failed to get IP for interface {interface}")
    return None

def send_email(new_ip):
    """Gmailを使ってメールを送信する"""
    hostname = socket.gethostname()
    subject = f"Raspberry Pi IP Address Changed : {hostname}"
    body = f"The new IP address of your Raspberry Pi is: {new_ip}"

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

def main():
    current_ip = get_current_ip()

    # 保存されたIPアドレスを読み込む
    if os.path.exists(IP_FILE):
        with open(IP_FILE, "r") as file:
            saved_ip = file.read().strip()
    else:
        saved_ip = None

    # IPアドレスが変更されている場合
    if current_ip != saved_ip:
        send_email(current_ip)

        # 新しいIPアドレスを保存
        with open(IP_FILE, "w") as file:
            file.write(current_ip)

if __name__ == "__main__":
    main()
