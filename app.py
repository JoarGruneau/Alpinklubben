from flask import Flask
from flask import render_template
from flask import request
import sqlite3
from flask import g, session, redirect, url_for, abort, flash, jsonify
from datetime import datetime
import os

import forms
import database

packages = [['package_1', 'Good off piste skies, a helmet and poles is included', 80],
            ['package_2', 'Good all around skies, a helmet and poles is included', 60],
            ['package_3', 'Good freestyle skies, a helmet and poles is included', 90],
            ['package_4', 'Good speed downhill skies, a helmet and poles is included', 120],
            ['package_5', 'Good cross country skies, a helmet and poles is included', 100]
            ]
passes = [['day_pass', 'Day pass', 700],
          ['week_pass', 'Week pass', 2200],
          ['season_pass', 'Season pass', 12000]]


DATABASE = 'alpinklubben.db'
DEBUG = True

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.secret_key = os.urandom(24)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form, prefix='login')
    register_form = forms.RegisterForm(request.form, prefix='register')
    if request.method == 'POST':
        if 'login' in request.form:
            login_form = forms.LoginForm(request.form, prefix='login')
            if login_form.validate() and login_form.authenticate():
                session['username'] = request.form['username']
                return redirect(url_for('register_news'))
        elif 'register' in request.form:
            if register_form.validate():
                register_form.save()
                session['username'] = register_form.username.data
                return redirect(url_for('home'))
    return render_template('login.html', login_form=login_form, register_form=register_form)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/ski_equipment', methods=['GET', 'POST'])
def ski_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    print (passes)
    for i in range(len(packages)):
        if request.method == 'POST' and packages[i][0] in request.form:
            form = forms.RentForm(request.form, prefix=str(i))
            if form.validate():
                if form.rent_form.data == "hours":
                    price = packages[i][2]
                else:
                    price = packages[i][2]*6
                database.insert_into_cart(session['username'], packages[i][1], price)
                print(packages[i][0])
                packages[i].append(forms.RentForm(prefix=str(i)))
            else:
                packages[i].append(form)
        else:
            packages[i].append(forms.RentForm(prefix=str(i)))
    return render_template('ski_equipment.html', packages=packages)

@app.route('/ski_passes', methods=['GET', 'POST'])
def ski_passes():
    if 'username' not in session:
        return redirect(url_for('login'))
    for i in range(len(passes)):
        if request.method == 'POST' and passes[i][0] in request.form:
            form = forms.PassForm(request.form, prefix=str(i))
            if form.validate():
                if form.buyer.data == "adult":
                    price = passes[i][2]
                else:
                    price = passes[i][2]/2
                database.insert_into_cart(session['username'], passes[i][1], price)
                print(passes[i][0])
                passes[i].append(forms.PassForm(prefix=str(i)))
            else:
                passes[i].append(form)
        else:
            passes[i].append(forms.PassForm(prefix=str(i)))
    return render_template('ski_passes.html', passes=passes)

@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    print (session['username'])
    print(database.get_cart(session['username']))
    return render_template('shopping_cart.html', shopping_cart=database.get_cart(session['username']))

@app.route('/delete/<item>', methods=['GET'])
def delete_nyhet(item):
    result = { 'status':0, 'message': 'Error'
    }
    try:
        db = database.get_db()
        db.execute('delete from cart where id=' + item)
        db.commit()
        result = { 'status':1, 'message': "Item Deleted"}
    except Exception as e:
        result = { 'status':0, 'message': repr(e)}
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)