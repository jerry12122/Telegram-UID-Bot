# Telegram-UID-Bot

[![hackmd-github-sync-badge](https://hackmd.io/pHQwYImLRYC_HZRz2HrTOw/badge)](https://hackmd.io/pHQwYImLRYC_HZRz2HrTOw)

這個機器人是利用`python-telegram-bot`套件所開發  
## 功能  
* 輸入指令:`/user` -回傳userID  
* 輸入其他訊息則回復`使用方法`  

## 安裝  
### 方法一  
1. 安裝套件
```
 pip install --user -r requirements.txt
```
2. Run
```
pyhton bot.py
```
### 方法二  
1. 建置Docker鏡像
```
 docker build -t telegram-bot .
```
2. 建立docker容器
```
docker run -itd \
    --name telegram-bot \
    telegram-bot:latest
```