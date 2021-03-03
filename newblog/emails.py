from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from newblog.extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    message = Message(subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, message])
    thr.start()
    return thr


def send_confirm_email(user, token, to=None):
    send_email(subject='Confirm account', to=to or user.email, template='emails/confirm', user=user, token=token)


def send_reset_password_email(user, token):
    send_email(subject='Reset password', to=user.email, template='emails/reset_password', user=user, token=token)


def send_change_email_email(user, token, to=None):
    send_email(subject='Change email', to=to or user.email, template='emails/change_email', user=user, token=token)
