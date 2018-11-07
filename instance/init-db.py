import sqlite3

db = sqlite3.connect('./xeekweb.sqlite.db')

cur =db.cursor()


with open('./schema.sql','r',encoding='utf-8') as f:
    cur.executescript(f.read())

with open('./author.sql','r',encoding='utf-8') as f:
    cur.executescript(f.read())

with open('./article.sql','r',encoding='utf-8') as f:
    cur.executescript(f.read())