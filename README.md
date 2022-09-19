# Telegram-UID-Bot

[![hackmd-github-sync-badge](https://hackmd.io/pHQwYImLRYC_HZRz2HrTOw/badge)](https://hackmd.io/pHQwYImLRYC_HZRz2HrTOw)

這個機器人是利用`python-telegram-bot`套件所開發

## 功能

- 輸入指令:`/user` -回傳 userID
- 輸入其他訊息則回復`使用方法`

## 安裝

### 複製`.env.sample`為`.env`並設定`TOKEN`

```
cp .env.sample .env
```

### 安裝套件

```
 pip3 install --user -r requirements.txt
```

### Run

```
pyhton3 bot.py
```

## 設定 systemd

### 編輯 bot.service

把`ExecStart=/usr/bin/python3 /root/tgbot/bot.py`更換為你的專案目錄

### 啟動服務

```bash
cp ./bot.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable bot
systemctl start bot
```

### 查看執行狀態

```bash
service bot status
```
