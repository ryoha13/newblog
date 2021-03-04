import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError
from newblog.extensions import db
from newblog.models import User, Photo, Tag, Comment, Notification, Category, Post, Link


faker = Faker(locale='zh-CN')


def fake_admin():
    admin = User(
        name='刘佳琪',
        username='ryoha13',
        email='ryoha13@163.com',
        confirmed=True,
        website='www.ryoha.cn',
        bio=faker.text(),
        location=faker.address(),
        member_since=faker.date_time_this_year(),
        last_seen=faker.date_time_this_month()
    )
    admin.password = '123456'
    db.session.add(admin)
    db.session.commit()


def fake_user(count=100):
    for i in range(count):
        user = User(
            name=faker.name(),
            username=faker.user_name(),
            email=faker.email(),
            confirmed=True,
            website=faker.url(),
            bio=faker.text(),
            location=faker.address(),
            member_since=faker.date_time_this_year(),
            last_seen=faker.date_time_this_month()
        )
        user.password = '123456'
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=300):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for i in range(count):
        tag = Tag(name=faker.word(), timestamp=faker.date_time_this_year())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=100):
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        print(i)
        filename = 'random_%d.jpg' % i
        r = lambda: random.randint(128, 255)
        img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=faker.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=faker.date_time_this_year()
        )
        for j in range(random.randint(1, 10)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)
        db.session.add(photo)
    db.session.commit()


def fake_collect(count=150):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_category(count=20):
    category = Category(name='默认')
    db.session.add(category)
    for i in range(count):
        category = Category(name=faker.word(), timestamp=faker.date_time_this_year())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_post(count=200):
    for i in range(count):
        post = Post(
            title=faker.sentence(),
            body=faker.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=faker.date_time_this_year()
        )


def fake_comment(count=1000):
    for i in range(count):
        comment = Comment(
            body=faker.sentence(),
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=faker.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.commit()

    salt = int(count * 0.2)
    for i in range(salt):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    for j in range(salt):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_link():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
