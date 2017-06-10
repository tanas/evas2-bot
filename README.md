# @evas2_bot

Добавь `@evas2_bot` в Telegram. Сможешь получать уведомления при появлении доступных дат 
для регистрации в литовском посольстве в Минске!

Команды:
 - /start - подписаться на уведомления о появлении доступных дат
 
 - /stop -  прекратить получение уведомлений
 

# Contribute or set up your own bot

### Dependencies

```
apt install python3 python3-pip
pip3 install telepot
```

### How to install

1) Copy `config.ini.dist` to `config.ini`
2) Create telegram bot and set the token
3) Create db
   ```
   python3 create_db.py
   ```
4) Schedule running `python3 emb.py` via cronetab