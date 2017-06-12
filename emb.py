import json
import ssl
from urllib.request import Request, urlopen
from datetime import datetime
import telepot
import sqlite3
import configparser
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(cur_dir+'/config.ini')

con = sqlite3.connect(cur_dir+'/'+config['sqlite']['db_name'])
cursor = con.cursor()
bot = telepot.Bot(config['bot']['token'])


def send_notify(dates):
    cursor.execute('SELECT dates FROM log ORDER BY id DESC LIMIT 1')
    last_log = cursor.fetchone()
    last_log_dates = json.loads(last_log[0])

    if len(last_log_dates) > 0:
        return

    cursor.execute('SELECT id FROM user WHERE notify = 1')

    for row in cursor:
        user_id = row[0]
        message = '%s\n%s\ngo to https://evas2.urm.lt/ru/visit/' % ('Embassy available dates:', ', '.join(dates))
        bot.sendMessage(user_id, message)


def parse_subscriptions():
    updates = bot.getUpdates()

    for update in updates:
        message = update['message']
        cursor.execute("INSERT OR IGNORE INTO telegram_update(id, message) VALUES(?,?)",
                       (update['update_id'], json.dumps(update['message']),))
        user = message['from']
        cursor.execute("INSERT OR IGNORE INTO user(id, profile, notify) VALUES(?,?,?)",
                       (user['id'], json.dumps(user), 0))

        text = message['text']
        command_to_notify = {
            '/start': 1,
            '/stop': 0,
        }
        if text in command_to_notify:
            cursor.execute("UPDATE user SET notify = ? WHERE id = ?",
                           (command_to_notify[text], user['id'],))

    con.commit()


def parse_dates():
    url = 'https://evas2.urm.lt/calendar/json?_d=&_aby=3&_cry=6&_c=1&_t='
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(url)
    req.add_header('X-Requested-With', 'XMLHttpRequest')

    with urlopen(req, context=ctx) as u:
        data = u.read().decode("utf-8")
        dates = json.loads(data)
        if len(dates) == 1 and len(dates[0]) == 0:
            dates = []

    return dates


def check():
    dates = parse_dates()
    print('%s %s' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '[' + ', '.join(dates) + ']'))

    if len(dates) > 0:
        send_notify(dates)

    cursor.execute("INSERT INTO log(dates, created_at) VALUES(?,?)",
                (json.dumps(dates), datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    con.commit()


parse_subscriptions()
check()
