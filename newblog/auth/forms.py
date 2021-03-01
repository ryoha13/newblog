from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 32)])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('注册')

    def validate_username(self, field):
        pass

    def validate_email(self, field):
        pass
