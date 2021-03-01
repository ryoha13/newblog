from flask import render_template
from ..auth import auth


@auth.route('/register')
def register():
    return render_template('auth/login.html')


@auth.route('/login')
def login():
    return render_template('auth/login.html')
