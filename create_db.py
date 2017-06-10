import sqlite3
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

cur_dir = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(cur_dir+'/'+config['sqlite']['db_name'])

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS log(id INTEGER PRIMARY KEY, dates TEXT, created_at DATE)")
    cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, profile TEXT, notify INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS telegram_update(id INTEGER PRIMARY KEY, message TEXT)")
