from flask import render_template
from ..auth import auth
from .forms import LoginForm, RegisterForm, ResetPasswordRequestForm


@auth.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/register.html', form=form)


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/login.html', form=form)


@auth.route('/reset-password-request')
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/reset-password-request.html', form=form)
