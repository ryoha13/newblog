import os
import click
from flask import Flask
from newblog.settings import configs
from newblog.extensions import db, mail, moment, login_manager, avatars, migrate, bootstrap, ckeditor, dropzone, \
    whooshee, csrf, toolbar
from newblog.models import Permission, Role, User, Post, Photo, Comment, Category, Collect, Notification, Link, Follow


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG' or 'dev')
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    register_bp(app)
    register_extensions(app)
    register_cmd(app)

    return app


def register_bp(app):
    from newblog.main import main
    from newblog.auth import auth
    from newblog.api import api
    from newblog.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    avatars.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    dropzone.init_app(app)
    whooshee.init_app(app)
    csrf.init_app(app)
    toolbar.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Permission=Permission, Role=Role, User=User, Post=Post, Photo=Photo, Comment=Comment,
                    Category=Category, Collect=Collect, Notification=Notification, Link=Link, Follow=Follow)


def register_cmd(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除DB并初始化')
    def initdb(drop):
        """开始初始化数据库"""
        if drop:
            click.confirm('本命令操作将会彻底drop数据库，请确认继续操作？', abort=True)
            db.drop_all()
            click.echo('Drop数据库完成')
        db.create_all()
        click.echo('数据库初始化完成')

    @app.cli.command()
    def init():
        """初始化数据库"""
        click.echo('正在开始初始化')
        db.create_all()
        click.echo('初始化权限和角色表...')
        Role.init_role()
        click.echo('初始化完成')

    @app.cli.command()
    def forge():
        """开始生成虚拟数据"""
        from newblog.fakes import fake_admin, fake_user, fake_follow, fake_tag, fake_photo, fake_collect, fake_category, \
            fake_post, fake_comment, fake_link
        db.drop_all()
        db.create_all()
        click.echo('初始化权限和角色')
        Role.init_role()
        click.echo('生成管理员')
        fake_admin()
        click.echo('生成用户列表')
        fake_user()
        click.echo('生成关系列表')
        fake_follow()
        click.echo('生成标签')
        fake_tag()
        click.echo('生成照片')
        fake_photo()
        click.echo('生成关注')
        fake_collect()
        click.echo('生成文章类别')
        fake_category()
        click.echo('生成文章列表')
        fake_post()
        click.echo('生成评论列表')
        fake_comment()
        click.echo('生成link列表')
        fake_link()
