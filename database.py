import sqlite3
from flask import g

from app import app


def insert_user(first_name, last_name, username, email, salted_hashed_password):
    db = get_db()
    db.execute('insert into users (first_name, last_name, username, email, hashed_password) values (?, ?, ?, ?, ?)',
               [first_name, last_name, username, email, str(salted_hashed_password)])
    db.commit()
    # print(db.execute('select * from users').fetchall())


def get_user(username):
    db = get_db()
    cur = db.execute('select * from users where username = ?', [username])
    # a = cur.fetchall()
    # print(list(a))
    return cur.fetchall()


def get_user_id(username):
    return get_user(username)[0][0]


def update_user(old_username, first_name, last_name, username, email):
    db = get_db()
    user_id = get_user_id(old_username)
    db.execute("update users set first_name =?, last_name =?, username =?, email =? where id =?",
               (first_name, last_name, username, email, user_id))
    db.commit()


def get_members():
    db = get_db()
    cur = db.execute('select first_name, last_name, email from users')
    return cur.fetchall()


def update_password(username, hashed_password):
    db = get_db()
    user_id = get_user_id(username)
    db.execute("update users set hashed_password =?where id =?",
               (hashed_password, user_id))
    db.commit()


def insert_into_cart(username, description, price):
    db = get_db()
    db.execute('insert into cart (username, description, price) values (?, ?, ?)',
               [get_user_id(username), description, price])
    db.commit()
    # print(db.execute('select * from cart').fetchall())


def get_cart(username):
    db = get_db()
    cur = db.execute('select * from cart where username = ?', [get_user_id(username)])
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
