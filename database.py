import sqlite3
from flask import g

from app import app


def insert_user(username, email, salted_hashed_password):
    db = get_db()
    db.execute('insert into users (username, email, password) values (?, ?, ?)',
               [username, email, salted_hashed_password])
    db.commit()
    # print(db.execute('select * from users').fetchall())


def get_user(username):
    db = get_db()
    cur = db.execute('select username, password from users where username = ?', [username])
    return cur.fetchall()


def insert_into_cart(username, description, price):
    db = get_db()
    db.execute('insert into cart (username, description, price) values (?, ?, ?)',
               [username, description, price])
    db.commit()
    # print(db.execute('select * from cart').fetchall())


def get_cart(username):
    db = get_db()
    cur = db.execute('select * from cart')
    # cur = db.execute('select description, price from cart where username = ?', [username])
    return cur.fetchall()


# connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('alpinklubben.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("created database")


# open conecction to db
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# closes connection to database
@app.teardown_appcontext
def close_db(_):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
