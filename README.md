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
