from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    users = db.relationship('User', backref='roles')

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrator']))
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship('Post', backref='author')


    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name='Guests').first()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.event.listen(User.name, 'set', User.on_created)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    body_html = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post')
    authod_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_body_change(target, value, oldvalue, initiator):
        if value is None or (value is ''):
            target.body_html = ''
        else:
            target.body_html = markdown(value)


db.event.listen(Post.body, 'set', Post.on_body_change)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

