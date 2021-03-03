from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user, confirm_login, login_fresh
from ..extensions import db
from ..models import User
from ..emails import send_confirm_email, send_reset_password_email, send_change_email_email
from ..utils import generate_token, validate_token, redirect_back
from ..settings import Operations
from ..auth import auth
from .forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm


@auth.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower(), password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('确认账户的邮件已经发到您的邮箱，请前往认证', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            if login_user(user, form.remember.data):
                flash('登录成功', 'info')
                return redirect_back()
            else:
                flash('您的账户已经被锁定', 'warning')
                return redirect(url_for('main.index'))
        flash('email无效或者密码错误', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('密码重置邮件已经发到您的邮箱，请前往认证', 'info')
            return redirect(url_for('auth.login'))
        flash('无效的邮箱地址', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset-password-request.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=form.password.data):
            flash('您的密码已经更新', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('无效的认证url，或者url过期，请重新申请', 'danger')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset-password.html', form=form)


@auth.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit() and current_user.verify_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经成功退出', 'info')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('您的账户认证已经通过', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('token无效或者过期', 'danger')
        return redirect(url_for('auth.resend_confirm_email'))


@auth.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('新的认证邮件已经发送的您的邮箱，请前往认证', 'info')
    return redirect(url_for('main.index'))

