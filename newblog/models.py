from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from newblog.extensions import db, login_manager

roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

    def __repr__(self):
        return '<Permission: %r>' % self.name


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')
    users = db.relationship('User', back_populates='role')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'WRITE'],
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'WRITE', 'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'WRITE', 'MODERATE', 'ADMINISTER']
        }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for p_name in roles_permissions_map[role_name]:
                p = Permission.query.filter_by(name=p_name).first()
                if p is None:
                    p = Permission(name=p_name)
                    db.session.add(p)
                role.permissions.append(p)
        db.session.commit()

    def add_p(self, p):
        pass

    def remove_p(self, p):
        pass

    def has_p(self, p):
        pass

    def reset_p(self):
        pass

    def __repr__(self):
        return '<Role: %r>' % self.name


class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='following', lazy='joined')


class Collect(db.Model):
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('photo.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    collector = db.relationship('User', back_populates='collections', lazy='joined')
    collected = db.relationship('Photo', back_populates='collectors', lazy='joined')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    website = db.Column(db.String(256))
    bio = db.Column(db.Text)
    location = db.Column(db.String(256))
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    avatar_raw = db.Column(db.String(64))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    locked = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    public_collections = db.Column(db.Boolean, default=True)
    receive_comment_notification = db.Column(db.Boolean, default=True)
    receive_follow_notification = db.Column(db.Boolean, default=True)
    receive_collect_notification = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')
    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower', lazy='dynamic',
                                cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed', lazy='dynamic',
                                cascade='all')
    collections = db.relationship('Collect', back_populates='collector', cascade='all')
    posts = ''
    photos = ''
    comments = ''

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('密码仅能写入，不能读取')

    @password.setter
    def password(self, p):
        self.password_hash = generate_password_hash(p)

    def verify_password(self, p):
        return check_password_hash(self.password_hash, p)

    def can(self, p_name):
        pass

    def is_admin(self):
        pass

    def ping(self):
        pass

    def gravatar(self):
        pass

    def follow(self, u):
        pass

    def unfollow(self, u):
        pass

    def is_following(self, p):
        pass

    def is_followed_by(self, p):
        pass

    def followed_posts(self):
        pass

    def followed_photos(self):
        pass

    def collect(self, p):
        pass

    def uncollect(self, p):
        pass

    def is_collecting(self, p):
        pass

    def lock(self):
        pass

    def unlock(self):
        pass

    def block(self):
        pass

    def unblock(self):
        pass

    def is_active(self):
        pass

    def __repr__(self):
        return '<User: %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def can(self, p):
        return False


login_manager.anonymous_user = AnonymousUser


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    flag = db.Column(db.Integer, default=0)
    can_comment = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = ''
    author = ''
    comments = ''
    category_id = ''
    category = ''


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    flag = db.Column(db.Integer, default=0)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    disabled = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = ''
    author = ''
    post_id = ''
    post = ''
    replied_id = ''
    replies = ''
    replied = ''
    photo_id = ''
    photo = ''


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    url = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


tagging = db.Table(
    'tagging',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    filename = db.Column(db.String(128))
    filename_s = db.Column(db.String(128))
    filename_m = db.Column(db.String(128))
    can_comment = db.Column(db.Boolean, default=True)
    flag = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tagging, back_populates='photo')
    collectors = db.relationship('Collect', back_populates='collected', cascade='all')
    author_id = ''
    author = ''
    comments = ''


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', back_populates='notifications')
