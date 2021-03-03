from functools import wraps
from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user


def confirm_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先确认账户，未收到确认邮件？<a class="alert-link" href="%s">重新发送邮件</a>' % url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(p_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(p_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required('ADMINISTER')(f)
